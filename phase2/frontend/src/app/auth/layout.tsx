/**
 * Auth Layout
 *
 * Layout for authentication pages (signup, login).
 * No authentication required to access these pages.
 */

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="auth-layout">
      {children}
    </div>
  );
}
