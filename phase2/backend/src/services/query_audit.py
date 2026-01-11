"""
Query audit service for verifying user isolation in database queries.

Ensures that all queries are properly filtered by user_id to prevent
unauthorized access to other users' data.

T029: Query Filtering Verification
"""

from sqlmodel import Session, select
from src.db.models import Task, User
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class QueryAudit:
    """
    Audit utility for verifying query filtering and data isolation.

    This class provides methods to verify that queries are properly
    filtering data by user_id to prevent cross-user access.
    """

    @staticmethod
    def verify_user_isolation_task(
        session: Session,
        user_id: str,
        task_ids: List[int],
    ) -> bool:
        """
        Verify that task_ids belong to the specified user.

        Args:
            session: Database session
            user_id: User's ID
            task_ids: List of task IDs to verify

        Returns:
            True if all tasks belong to user, False otherwise

        Usage:
            # Verify that returned tasks belong to authenticated user
            tasks = TaskService.get_user_tasks(session, user_id)
            task_ids = [t.id for t in tasks]
            QueryAudit.verify_user_isolation_task(session, user_id, task_ids)
        """
        if not task_ids:
            return True

        # Query to find how many of these task IDs belong to this user
        query = select(Task).where(
            Task.id.in_(task_ids),
            Task.user_id == user_id,
        )
        matching_tasks = session.exec(query).all()

        # All provided task_ids should match
        found_count = len(matching_tasks)
        expected_count = len(task_ids)

        if found_count != expected_count:
            logger.error(
                f"Query isolation violation: user {user_id} has {found_count}/{expected_count} "
                f"tasks from requested IDs {task_ids}"
            )
            return False

        logger.debug(f"Query isolation verified: user {user_id} owns all {found_count} tasks")
        return True

    @staticmethod
    def verify_task_ownership(
        session: Session,
        task_id: int,
        user_id: str,
    ) -> bool:
        """
        Verify that a task belongs to a user.

        Args:
            session: Database session
            task_id: ID of task to verify
            user_id: User's ID

        Returns:
            True if task belongs to user, False otherwise

        Usage:
            # Before returning/modifying a task
            if not QueryAudit.verify_task_ownership(session, task_id, user_id):
                raise Exception("Task not owned by user")
        """
        query = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id,
        )
        task = session.exec(query).first()

        if task is None:
            logger.warning(
                f"Task ownership violation: user {user_id} attempted to access task {task_id}"
            )
            return False

        logger.debug(f"Task ownership verified: task {task_id} belongs to user {user_id}")
        return True

    @staticmethod
    def audit_query_filtering(query_str: str, user_id: str) -> bool:
        """
        Audit a SQL query string to verify it includes user_id filtering.

        Args:
            query_str: SQL query string (for logging/debugging)
            user_id: User_id that should be in the filter

        Returns:
            True if query appears to have user_id filter

        Usage:
            # Log all queries for audit trail
            query_str = str(query.statement)
            QueryAudit.audit_query_filtering(query_str, user_id)
        """
        # Check that user_id is mentioned in the query
        if "user_id" not in query_str.lower():
            logger.error(
                f"CRITICAL: Query missing user_id filter for user {user_id}: {query_str}"
            )
            return False

        logger.debug(f"Query properly filtered by user_id for user {user_id}")
        return True

    @staticmethod
    def log_cross_user_attempt(
        user_id: str,
        target_user_id: str,
        resource_type: str,
        operation: str,
    ) -> None:
        """
        Log an attempted cross-user access (security event).

        Args:
            user_id: Authenticated user's ID
            target_user_id: Owner of the resource
            resource_type: Type of resource (task, user, etc.)
            operation: Operation attempted (read, update, delete, etc.)

        Usage:
            # When detecting cross-user access attempt
            if user_id != target_user_id:
                QueryAudit.log_cross_user_attempt(
                    user_id, target_user_id, "task", "delete"
                )
        """
        logger.warning(
            f"SECURITY: Cross-user access attempt - "
            f"user {user_id} attempted {operation} on {resource_type} owned by {target_user_id}"
        )

    @staticmethod
    def verify_query_results_isolation(
        results: List[Any],
        user_id: str,
        resource_type: str = "task",
    ) -> bool:
        """
        Verify that query results are isolated to the user.

        Args:
            results: List of result objects from database query
            user_id: Expected owner user_id
            resource_type: Type of resource (task, user, etc.)

        Returns:
            True if all results belong to user

        Usage:
            # After fetching results from database
            tasks = session.exec(query).all()
            QueryAudit.verify_query_results_isolation(tasks, user_id, "task")
        """
        if not results:
            return True

        for result in results:
            # Check if result has user_id attribute
            if not hasattr(result, "user_id"):
                logger.error(
                    f"Query verification failed: {resource_type} result missing user_id attribute"
                )
                return False

            if result.user_id != user_id:
                logger.error(
                    f"Query isolation violation: {resource_type} {result.id} "
                    f"belongs to {result.user_id}, not {user_id}"
                )
                return False

        logger.debug(
            f"Query results verified: all {len(results)} {resource_type}s belong to user {user_id}"
        )
        return True


class QueryFilteringReport:
    """
    Generate reports on query filtering compliance.

    Helps identify any queries that might not be properly filtering by user_id.
    """

    @staticmethod
    def generate_isolation_report(session: Session) -> Dict[str, Any]:
        """
        Generate a report on data isolation across all tables.

        Returns:
            Dict with statistics on user data isolation

        Usage:
            report = QueryFilteringReport.generate_isolation_report(session)
            print(f"Total tasks: {report['total_tasks']}")
            print(f"Users: {report['users_with_tasks']}")
        """
        # Count total tasks
        total_tasks = len(session.exec(select(Task)).all())

        # Count users with tasks
        users_with_tasks = {}
        all_tasks = session.exec(select(Task)).all()
        for task in all_tasks:
            if task.user_id not in users_with_tasks:
                users_with_tasks[task.user_id] = 0
            users_with_tasks[task.user_id] += 1

        # Count orphaned tasks (should be 0)
        orphaned_tasks = len(
            session.exec(
                select(Task).where(Task.user_id.is_(None))
            ).all()
        )

        report = {
            "total_tasks": total_tasks,
            "total_users": len(users_with_tasks),
            "tasks_per_user": users_with_tasks,
            "orphaned_tasks": orphaned_tasks,
            "isolation_status": "HEALTHY" if orphaned_tasks == 0 else "VIOLATION",
        }

        logger.info(f"Isolation report generated: {report}")
        return report

    @staticmethod
    def verify_no_orphaned_data(session: Session) -> bool:
        """
        Verify that no tasks exist without a user_id (orphaned data).

        Returns:
            True if no orphaned data, False if issues found

        Usage:
            if not QueryFilteringReport.verify_no_orphaned_data(session):
                logger.error("Database has orphaned records!")
        """
        orphaned_tasks = session.exec(
            select(Task).where(Task.user_id.is_(None))
        ).all()

        if orphaned_tasks:
            logger.error(f"Found {len(orphaned_tasks)} orphaned tasks in database")
            return False

        logger.info("Database verification passed: no orphaned data")
        return True
