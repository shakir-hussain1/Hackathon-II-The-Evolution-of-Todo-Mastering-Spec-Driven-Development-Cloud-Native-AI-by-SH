# Troubleshooting Guide

Comprehensive troubleshooting guide for the Todo App Kubernetes deployment.

## Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Pod Issues](#pod-issues)
- [Image Issues](#image-issues)
- [Networking Issues](#networking-issues)
- [Storage Issues](#storage-issues)
- [Secret Issues](#secret-issues)
- [Performance Issues](#performance-issues)
- [Helm Issues](#helm-issues)
- [Minikube Issues](#minikube-issues)

## Quick Diagnostics

### Run Verification Script
```bash
./scripts/verify.sh
```

### Check Overall Status
```bash
# All resources
kubectl get all -l app.kubernetes.io/instance=todo-app

# Detailed view
kubectl describe deployment todo-app-backend
kubectl describe deployment todo-app-frontend

# Recent events
kubectl get events --sort-by='.lastTimestamp' | tail -20
```

### Check Logs
```bash
# Backend logs
kubectl logs -l app.kubernetes.io/component=backend --tail=50

# Frontend logs
kubectl logs -l app.kubernetes.io/component=frontend --tail=50

# Previous crash logs
kubectl logs <pod-name> --previous
```

## Pod Issues

### Issue: Pods Stuck in Pending

**Symptoms**:
- Pods show `Pending` status for extended time
- `kubectl get pods` shows `0/1` or `0/2` ready

**Diagnosis**:
```bash
kubectl describe pod <pod-name>
```

**Common Causes & Solutions**:

1. **Insufficient Resources**
   ```bash
   # Check node capacity
   kubectl describe nodes
   kubectl top nodes

   # Solution: Increase Minikube resources
   minikube stop
   minikube start --cpus=4 --memory=8192
   ```

2. **PVC Not Binding**
   ```bash
   # Check PVC status
   kubectl get pvc

   # Check storage class
   kubectl get storageclass

   # Solution: Delete and recreate PVC
   kubectl delete pvc todo-app-backend-pvc
   helm upgrade todo-app ./helm/todo-app --reuse-values
   ```

3. **Image Pull Issues**
   ```bash
   # Check events
   kubectl describe pod <pod-name> | grep -A 5 Events

   # Solution: See Image Issues section
   ```

### Issue: Pods in CrashLoopBackOff

**Symptoms**:
- Pods repeatedly restart
- Status shows `CrashLoopBackOff`
- Restart count keeps increasing

**Diagnosis**:
```bash
# View current logs
kubectl logs <pod-name>

# View logs from previous crash
kubectl logs <pod-name> --previous

# Check container exit code
kubectl get pod <pod-name> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.exitCode}'
```

**Common Causes & Solutions**:

1. **Missing Environment Variables**
   ```bash
   # Check environment
   kubectl exec <pod-name> -- env

   # Check secrets exist
   kubectl get secret todo-secrets

   # Solution: Recreate secrets
   kubectl delete secret todo-secrets
   helm upgrade todo-app ./helm/todo-app \
     --set secrets.openaiApiKey="$OPENAI_API_KEY" \
     --set secrets.jwtSecret="$JWT_SECRET"
   ```

2. **Application Error**
   ```bash
   # Check logs for stack traces
   kubectl logs <pod-name> | grep -i error

   # Solution: Fix application code and rebuild
   eval $(minikube docker-env)
   ./scripts/build-images.sh
   kubectl rollout restart deployment/todo-app-backend
   ```

3. **Health Check Failure**
   ```bash
   # Test health endpoint manually
   kubectl exec <pod-name> -- wget -q -O- http://localhost:7860/health

   # Solution: Adjust health check settings
   helm upgrade todo-app ./helm/todo-app \
     --set backend.livenessProbe.initialDelaySeconds=60 \
     --reuse-values
   ```

### Issue: Pods Not Ready

**Symptoms**:
- Pods running but showing `0/1` ready
- Readiness probe failing

**Diagnosis**:
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**Solutions**:

1. **Application Still Starting**
   ```bash
   # Wait longer
   kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo-app --timeout=300s
   ```

2. **Readiness Probe Misconfigured**
   ```bash
   # Test endpoint
   kubectl exec <pod-name> -- curl http://localhost:7860/health

   # Increase initial delay
   helm upgrade todo-app ./helm/todo-app \
     --set backend.readinessProbe.initialDelaySeconds=30 \
     --reuse-values
   ```

## Image Issues

### Issue: ImagePullBackOff

**Symptoms**:
- Pod status: `ImagePullBackOff` or `ErrImagePull`
- Cannot pull image

**Diagnosis**:
```bash
kubectl describe pod <pod-name> | grep -A 10 Events
```

**Causes & Solutions**:

1. **Image Not in Minikube's Docker**
   ```bash
   # Check if image exists
   eval $(minikube docker-env)
   docker images | grep todo-

   # Solution: Build images in Minikube's Docker
   eval $(minikube docker-env)
   ./scripts/build-images.sh
   ```

2. **Wrong Image Pull Policy**
   ```bash
   # Check pull policy
   kubectl get deployment todo-app-backend -o jsonpath='{.spec.template.spec.containers[0].imagePullPolicy}'

   # Solution: Set to IfNotPresent
   helm upgrade todo-app ./helm/todo-app \
     --set backend.image.pullPolicy=IfNotPresent \
     --reuse-values
   ```

3. **Typo in Image Name**
   ```bash
   # Check configured image
   kubectl get deployment todo-app-backend -o jsonpath='{.spec.template.spec.containers[0].image}'

   # Verify image exists
   docker images
   ```

### Issue: Old Image Version Running

**Symptoms**:
- Rebuilt image but pods still use old version
- Changes not reflected

**Solution**:
```bash
# Ensure using Minikube's Docker
eval $(minikube docker-env)

# Rebuild with new tag
docker build -t todo-backend:v2 -f phase4/docker/backend.Dockerfile .

# Update deployment
helm upgrade todo-app ./helm/todo-app \
  --set backend.image.tag=v2 \
  --reuse-values

# Or force restart with same image
kubectl rollout restart deployment/todo-app-backend
```

## Networking Issues

### Issue: Frontend Can't Reach Backend

**Symptoms**:
- Frontend loads but API calls fail
- Network errors in browser console

**Diagnosis**:
```bash
# Test backend from frontend pod
kubectl exec -it deployment/todo-app-frontend -- wget -q -O- http://todo-app-backend:8000/health

# Check service endpoints
kubectl get endpoints todo-app-backend

# Check DNS resolution
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup todo-app-backend
```

**Solutions**:

1. **Service Not Ready**
   ```bash
   # Check service
   kubectl get svc todo-app-backend

   # Check if pods are selected
   kubectl get endpoints todo-app-backend

   # Verify labels match
   kubectl get pods --show-labels
   ```

2. **Wrong Service Name**
   ```bash
   # Check frontend env var
   kubectl exec deployment/todo-app-frontend -- printenv NEXT_PUBLIC_API_URL

   # Should be: http://todo-app-backend:8000
   # Update if wrong
   helm upgrade todo-app ./helm/todo-app \
     --set frontend.env[1].value="http://todo-app-backend:8000" \
     --reuse-values
   ```

3. **CORS Issues**
   ```bash
   # Check backend CORS settings
   kubectl exec deployment/todo-app-backend -- printenv CORS_ORIGINS

   # Update CORS origins
   helm upgrade todo-app ./helm/todo-app \
     --set backend.env[4].value="http://localhost:3000,http://localhost:30080,*" \
     --reuse-values
   ```

### Issue: Can't Access Frontend from Browser

**Symptoms**:
- `minikube service` command doesn't work
- Browser can't connect to NodePort

**Diagnosis**:
```bash
# Check service type
kubectl get svc todo-app-frontend

# Get Minikube IP
minikube ip

# Check NodePort
kubectl get svc todo-app-frontend -o jsonpath='{.spec.ports[0].nodePort}'
```

**Solutions**:

1. **Minikube Not Running**
   ```bash
   minikube status
   minikube start
   ```

2. **Wrong URL**
   ```bash
   # Get correct URL
   minikube service todo-app-frontend --url

   # Or manually construct
   echo "http://$(minikube ip):$(kubectl get svc todo-app-frontend -o jsonpath='{.spec.ports[0].nodePort}')"
   ```

3. **Firewall Blocking**
   ```bash
   # Try port forwarding instead
   kubectl port-forward svc/todo-app-frontend 3000:3000
   # Then access: http://localhost:3000
   ```

## Storage Issues

### Issue: PVC Not Binding

**Symptoms**:
- PVC status: `Pending`
- Backend pod can't start

**Diagnosis**:
```bash
kubectl get pvc
kubectl describe pvc todo-app-backend-pvc
```

**Solutions**:

1. **No Storage Class**
   ```bash
   # Check available storage classes
   kubectl get storageclass

   # Minikube should have 'standard'
   # If not, enable storage provisioner
   minikube addons enable storage-provisioner
   ```

2. **Wrong Storage Class**
   ```bash
   # Update to correct storage class
   helm upgrade todo-app ./helm/todo-app \
     --set backend.persistence.storageClass="standard" \
     --reuse-values
   ```

### Issue: Database Data Lost After Restart

**Symptoms**:
- Todos disappear after pod restart
- Database resets

**Diagnosis**:
```bash
# Check if PVC exists and is bound
kubectl get pvc todo-app-backend-pvc

# Check volume mount
kubectl describe pod <backend-pod-name> | grep -A 5 Mounts
```

**Solutions**:

1. **PVC Not Mounted**
   ```bash
   # Verify persistence is enabled
   helm get values todo-app | grep persistence

   # Enable if disabled
   helm upgrade todo-app ./helm/todo-app \
     --set backend.persistence.enabled=true \
     --reuse-values
   ```

2. **Wrong Mount Path**
   ```bash
   # Check mount path matches DATABASE_URL
   kubectl exec deployment/todo-app-backend -- ls -la /app/data

   # Update if needed
   helm upgrade todo-app ./helm/todo-app \
     --set backend.persistence.mountPath=/app/data \
     --reuse-values
   ```

## Secret Issues

### Issue: OpenAI API Calls Failing

**Symptoms**:
- Backend errors about API key
- Authentication failures with OpenAI

**Diagnosis**:
```bash
# Check if secret exists
kubectl get secret todo-secrets

# Decode and verify API key
kubectl get secret todo-secrets -o jsonpath='{.data.openai-api-key}' | base64 -d

# Check backend logs
kubectl logs -l app.kubernetes.io/component=backend | grep -i openai
```

**Solutions**:

1. **Secret Not Set**
   ```bash
   # Create/update secret
   helm upgrade todo-app ./helm/todo-app \
     --set secrets.openaiApiKey="$OPENAI_API_KEY" \
     --set secrets.jwtSecret="$JWT_SECRET"

   # Restart pods
   kubectl rollout restart deployment/todo-app-backend
   ```

2. **Invalid API Key**
   ```bash
   # Test API key manually
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"

   # Update with valid key
   kubectl delete secret todo-secrets
   helm upgrade todo-app ./helm/todo-app \
     --set secrets.openaiApiKey="sk-valid-key-here" \
     --reuse-values
   ```

### Issue: JWT Token Errors

**Symptoms**:
- Authentication failures
- Token verification errors

**Diagnosis**:
```bash
# Check JWT secret exists
kubectl get secret todo-secrets -o jsonpath='{.data.jwt-secret}' | base64 -d

# Check backend logs
kubectl logs -l app.kubernetes.io/component=backend | grep -i jwt
```

**Solution**:
```bash
# Generate new JWT secret
JWT_SECRET=$(openssl rand -hex 32)

# Update secret
helm upgrade todo-app ./helm/todo-app \
  --set secrets.jwtSecret="$JWT_SECRET" \
  --reuse-values

# Restart backend
kubectl rollout restart deployment/todo-app-backend
```

## Performance Issues

### Issue: Pods Using Too Much Memory

**Symptoms**:
- Pods getting `OOMKilled`
- High memory usage

**Diagnosis**:
```bash
# Check current usage
kubectl top pods

# Check limits
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[0].resources}'

# View events
kubectl get events | grep OOM
```

**Solutions**:

1. **Increase Memory Limits**
   ```bash
   helm upgrade todo-app ./helm/todo-app \
     --set backend.resources.limits.memory=1Gi \
     --set backend.resources.requests.memory=512Mi \
     --reuse-values
   ```

2. **Memory Leak in Application**
   ```bash
   # Check logs for memory warnings
   kubectl logs <pod-name> | grep -i memory

   # Fix application code and rebuild
   ```

### Issue: Slow Application Response

**Symptoms**:
- API calls taking too long
- Frontend slow to load

**Diagnosis**:
```bash
# Check CPU usage
kubectl top pods

# Check if CPU throttled
kubectl describe pod <pod-name> | grep -i cpu

# Test endpoint response time
time kubectl exec deployment/todo-app-backend -- wget -q -O- http://localhost:7860/health
```

**Solutions**:

1. **Increase CPU Limits**
   ```bash
   helm upgrade todo-app ./helm/todo-app \
     --set backend.resources.limits.cpu=1000m \
     --set backend.resources.requests.cpu=500m \
     --reuse-values
   ```

2. **Scale Up Replicas**
   ```bash
   kubectl scale deployment/todo-app-backend --replicas=4
   ```

## Helm Issues

### Issue: Helm Install/Upgrade Fails

**Symptoms**:
- Helm command errors out
- Release in failed state

**Diagnosis**:
```bash
# Check Helm release status
helm list

# Get detailed status
helm status todo-app

# View release history
helm history todo-app
```

**Solutions**:

1. **Invalid Values**
   ```bash
   # Validate chart
   helm lint ./helm/todo-app

   # Dry run to see errors
   helm upgrade todo-app ./helm/todo-app --dry-run --debug
   ```

2. **Release Stuck**
   ```bash
   # Rollback to previous version
   helm rollback todo-app

   # Or delete and reinstall
   helm uninstall todo-app
   ./scripts/deploy.sh
   ```

3. **Timeout Issues**
   ```bash
   # Increase timeout
   helm upgrade todo-app ./helm/todo-app --timeout 10m --wait
   ```

### Issue: Can't Find Helm Chart

**Symptoms**:
- "chart not found" error
- Wrong path

**Solution**:
```bash
# Ensure you're in correct directory
cd phase4

# Use absolute path
helm install todo-app /absolute/path/to/helm/todo-app

# Or relative path from correct location
helm install todo-app ./helm/todo-app
```

## Minikube Issues

### Issue: Minikube Won't Start

**Symptoms**:
- `minikube start` fails
- VM creation errors

**Solutions**:

1. **Delete and Recreate**
   ```bash
   minikube delete
   minikube start --cpus=4 --memory=8192
   ```

2. **Check System Resources**
   ```bash
   # Ensure enough RAM and CPU available
   # Close other applications

   minikube start --cpus=2 --memory=4096  # Use less resources
   ```

3. **Driver Issues**
   ```bash
   # Try different driver
   minikube start --driver=docker
   # or
   minikube start --driver=virtualbox
   ```

### Issue: Docker Commands Not Working After `eval $(minikube docker-env)`

**Symptoms**:
- Docker commands hang or fail
- Can't connect to Docker daemon

**Solution**:
```bash
# Reset Docker environment
eval $(minikube docker-env -u)

# Or restart terminal

# Then reconnect
eval $(minikube docker-env)
```

### Issue: Minikube Service Not Accessible

**Symptoms**:
- `minikube service` hangs
- Can't access service URL

**Solutions**:

1. **Use Port Forwarding Instead**
   ```bash
   kubectl port-forward svc/todo-app-frontend 3000:3000
   ```

2. **Check Minikube Network**
   ```bash
   minikube ip
   ping $(minikube ip)
   ```

3. **Restart Minikube**
   ```bash
   minikube stop
   minikube start
   ```

## General Debugging Workflow

When encountering any issue, follow this workflow:

1. **Check Pod Status**
   ```bash
   kubectl get pods -l app.kubernetes.io/instance=todo-app
   ```

2. **View Pod Details**
   ```bash
   kubectl describe pod <pod-name>
   ```

3. **Check Logs**
   ```bash
   kubectl logs <pod-name>
   kubectl logs <pod-name> --previous  # For crashed pods
   ```

4. **Check Events**
   ```bash
   kubectl get events --sort-by='.lastTimestamp' | tail -20
   ```

5. **Verify Resources**
   ```bash
   kubectl get all -l app.kubernetes.io/instance=todo-app
   kubectl get pvc
   kubectl get secrets
   ```

6. **Test Connectivity**
   ```bash
   kubectl exec -it <pod-name> -- /bin/bash
   # Then test manually
   ```

7. **Review Configuration**
   ```bash
   helm get values todo-app
   kubectl get configmaps
   kubectl describe deployment todo-app-backend
   ```

## Getting Help

If you're still stuck after trying these solutions:

1. **Collect Diagnostic Information**
   ```bash
   # Save all information to files
   kubectl get all -l app.kubernetes.io/instance=todo-app > resources.txt
   kubectl describe deployment todo-app-backend > backend-deployment.txt
   kubectl logs -l app.kubernetes.io/component=backend --tail=100 > backend-logs.txt
   helm status todo-app > helm-status.txt
   ```

2. **Run Verification Script**
   ```bash
   ./scripts/verify.sh > verify-output.txt 2>&1
   ```

3. **Check Documentation**
   - Review [DEPLOYMENT.md](../DEPLOYMENT.md)
   - Check [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)

---

**Remember**: Most issues can be resolved by:
1. Rebuilding images in Minikube's Docker
2. Checking and updating secrets
3. Verifying resource limits
4. Reviewing logs for error messages
