# Frontend API Integration Skill - Specification

## Skill Overview
**Name:** frontend-api-integration
**Type:** Integration Validation Skill
**Category:** Frontend-Backend Communication

## Purpose
Validates frontend-backend interaction by checking API base URL usage, JWT attachment, error handling, and detecting CORS or network misconfigurations.

## Input Requirements
- Frontend API client code
- API service/helper files
- HTTP interceptor configurations
- Environment variable files
- CORS configuration (backend)

## Core Functions

### 1. API Base URL Validation
- Verify base URL configuration
- Check environment variable usage
- Validate URL format
- Confirm protocol (http/https)
- Review multi-environment support

### 2. JWT Attachment Verification
- Check Authorization header usage
- Verify Bearer token format
- Validate token retrieval from storage
- Review interceptor implementation
- Check token refresh logic

### 3. Error Handling Validation
- Verify HTTP error interception
- Check error response parsing
- Validate user-facing error messages
- Review retry logic
- Confirm timeout handling

### 4. CORS Configuration Review
- Check CORS headers in backend
- Verify allowed origins
- Validate allowed methods
- Confirm credentials handling
- Review preflight request handling

### 5. Network Misconfiguration Detection
- Identify hardcoded URLs
- Find mixed content issues (http/https)
- Detect missing error boundaries
- Check for exposed credentials
- Verify request/response logging

## Validation Rules

### API Base URL Standards
```typescript
// ✓ CORRECT - Environment variable
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// ✓ CORRECT - Config file
export const config = {
  apiBaseUrl: process.env.REACT_APP_API_BASE_URL,
}

// ✗ INCORRECT - Hardcoded
const API_BASE_URL = 'http://localhost:8000'  // Won't work in production

// ✗ INCORRECT - Mixed protocols
const API_BASE_URL = 'http://api.example.com'  // Should be https in prod
```

### JWT Attachment Standards
```typescript
// ✓ CORRECT - Axios interceptor
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ✓ CORRECT - Fetch with headers
const response = await fetch(`${API_BASE_URL}/todos`, {
  headers: {
    'Authorization': `Bearer ${getToken()}`,
    'Content-Type': 'application/json'
  }
})

// ✗ INCORRECT - Missing Authorization header
const response = await fetch(`${API_BASE_URL}/todos`)

// ✗ INCORRECT - Token in URL (security risk)
const response = await fetch(`${API_BASE_URL}/todos?token=${token}`)
```

### Error Handling Standards
```typescript
// ✓ CORRECT - Comprehensive error handling
try {
  const response = await api.get('/todos')
  return response.data
} catch (error) {
  if (error.response) {
    // Server responded with error status
    const status = error.response.status
    const message = error.response.data?.detail || 'An error occurred'

    if (status === 401) {
      // Handle unauthorized (logout, redirect)
      handleLogout()
    } else if (status === 404) {
      // Handle not found
      showError('Resource not found')
    } else {
      // Handle other errors
      showError(message)
    }
  } else if (error.request) {
    // Request made but no response
    showError('Network error. Please check your connection.')
  } else {
    // Something else happened
    showError('An unexpected error occurred')
  }
  throw error
}

// ✗ INCORRECT - Silent failure
try {
  const response = await api.get('/todos')
  return response.data
} catch (error) {
  console.log(error)  // User sees nothing
}

// ✗ INCORRECT - Generic error
try {
  const response = await api.get('/todos')
  return response.data
} catch (error) {
  alert('Error')  // Not helpful
}
```

### CORS Configuration Standards (Backend)
```python
# ✓ CORRECT - FastAPI CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# ✗ INCORRECT - Overly permissive
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any origin
    allow_credentials=True,  # Security risk with "*"
)
```

## Validation Process

### Step 1: API Client Audit
1. Locate API client configuration
2. Check base URL setup
3. Review HTTP client initialization
4. Validate interceptors/middleware
5. Check environment configuration

### Step 2: Authentication Review
1. Find token storage mechanism
2. Check token retrieval logic
3. Verify Authorization header attachment
4. Review token refresh implementation
5. Validate logout/cleanup

### Step 3: Error Handling Analysis
1. Test error scenarios
2. Check error interceptors
3. Verify user feedback
4. Review retry logic
5. Test network failures

### Step 4: CORS Testing
1. Check backend CORS config
2. Test cross-origin requests
3. Verify preflight requests
4. Check credentials handling
5. Test with actual frontend origin

### Step 5: Security Audit
1. Check for exposed credentials
2. Verify HTTPS usage
3. Review token storage security
4. Check for XSS vulnerabilities
5. Validate CSP headers

## Output Format

### Integration Validation Report
```markdown
## FRONTEND API INTEGRATION REPORT

**Overall Status:** [HEALTHY | ISSUES FOUND | CRITICAL]
**API Client:** Axios
**Base URL Configuration:** ✓ Environment variable
**JWT Attachment:** ✓ Interceptor configured
**Error Handling:** ⚠ Partial implementation
**CORS Status:** ✗ Misconfigured

### ✓ Correct Configurations
1. **API Base URL**
   - Location: src/config/api.ts
   - Method: Environment variable (VITE_API_BASE_URL)
   - Development: http://localhost:8000
   - Production: https://api.example.com
   - Status: ✓ Properly configured

2. **JWT Attachment**
   - Location: src/api/client.ts:15
   - Method: Axios request interceptor
   - Header: Authorization: Bearer {token}
   - Storage: localStorage
   - Status: ✓ Correctly implemented

### ⚠ Issues Found
3. **Error Handling**
   - Location: src/api/todos.ts:45
   - Issue: Generic error messages
   - Impact: Poor user experience
   - Fix: Parse error.response.data.detail for specific messages

4. **Token Refresh**
   - Location: N/A
   - Issue: No refresh token logic
   - Impact: Users logged out after 15 min
   - Fix: Implement refresh token interceptor

### ✗ Critical Issues
5. **CORS Configuration**
   - Location: backend/main.py:12
   - Issue: allow_origins=["*"] with credentials
   - Impact: Security vulnerability
   - Fix: Specify allowed origins explicitly
   ```python
   allow_origins=[
       "http://localhost:5173",
       "https://app.example.com"
   ]
   ```

6. **Mixed Content**
   - Location: src/api/client.ts:8
   - Issue: API_BASE_URL uses http in production
   - Impact: Requests blocked on HTTPS site
   - Fix: Ensure HTTPS in production environment
```

### Connectivity Risks
```markdown
## CONNECTIVITY RISKS

### HIGH RISK
1. **Token in localStorage**
   - Risk: Vulnerable to XSS attacks
   - Location: src/auth/storage.ts
   - Recommendation: Use httpOnly secure cookies instead
   - Mitigation: If localStorage required, implement CSP headers

2. **No Request Timeout**
   - Risk: Hanging requests on network issues
   - Location: src/api/client.ts
   - Recommendation: Set timeout (e.g., 30 seconds)
   ```typescript
   axios.create({
     baseURL: API_BASE_URL,
     timeout: 30000  // Add this
   })
   ```

### MEDIUM RISK
3. **Missing Retry Logic**
   - Risk: Transient network errors not handled
   - Location: src/api/client.ts
   - Recommendation: Implement exponential backoff retry

4. **No Offline Detection**
   - Risk: Poor UX when offline
   - Location: N/A
   - Recommendation: Add navigator.onLine checks
```

### Fix Recommendations
```markdown
## FIX RECOMMENDATIONS (Prioritized)

### CRITICAL (Fix immediately)
1. **Fix CORS Configuration**
   ```python
   # backend/main.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:5173", "https://app.example.com"],
       allow_credentials=True,
       allow_methods=["GET", "POST", "PUT", "DELETE"],
       allow_headers=["Authorization", "Content-Type"],
   )
   ```

2. **Use HTTPS in Production**
   ```bash
   # .env.production
   VITE_API_BASE_URL=https://api.example.com
   ```

### HIGH (Fix before release)
3. **Implement Token Refresh**
   ```typescript
   // src/api/client.ts
   axios.interceptors.response.use(
     response => response,
     async error => {
       if (error.response?.status === 401) {
         const refreshToken = getRefreshToken()
         if (refreshToken) {
           try {
             const { data } = await axios.post('/auth/refresh', { refreshToken })
             setToken(data.access_token)
             error.config.headers.Authorization = `Bearer ${data.access_token}`
             return axios.request(error.config)
           } catch (refreshError) {
             handleLogout()
           }
         }
       }
       return Promise.reject(error)
     }
   )
   ```

4. **Add Request Timeout**
   ```typescript
   const api = axios.create({
     baseURL: API_BASE_URL,
     timeout: 30000,
     headers: { 'Content-Type': 'application/json' }
   })
   ```

### MEDIUM (Improve for better UX)
5. **Better Error Messages**
   ```typescript
   const getErrorMessage = (error) => {
     if (error.response) {
       return error.response.data?.detail || 'Server error occurred'
     } else if (error.request) {
       return 'Network error. Please check your connection.'
     } else {
       return 'An unexpected error occurred'
     }
   }
   ```

6. **Add Retry Logic**
   ```typescript
   import axiosRetry from 'axios-retry'

   axiosRetry(api, {
     retries: 3,
     retryDelay: axiosRetry.exponentialDelay,
     retryCondition: (error) => {
       return axiosRetry.isNetworkOrIdempotentRequestError(error)
         || error.response?.status === 429
     }
   })
   ```

### LOW (Nice to have)
7. **Offline Detection**
   ```typescript
   window.addEventListener('online', () => {
     showNotification('Connection restored')
     retryFailedRequests()
   })

   window.addEventListener('offline', () => {
     showNotification('You are offline')
   })
   ```
```

## Common Integration Issues

### Issue 1: CORS Errors
```
Error: Access to fetch at 'http://localhost:8000/api/todos'
from origin 'http://localhost:5173' has been blocked by CORS policy
```

**Fix:** Configure CORS on backend
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 2: 401 Unauthorized
```
Error: Request failed with status code 401
```

**Fix:** Ensure JWT is attached
```typescript
// Check token is being sent
axios.interceptors.request.use(config => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

### Issue 3: Network Error
```
Error: Network Error
```

**Causes & Fixes:**
- Backend not running → Start backend server
- Wrong API URL → Check environment variable
- CORS misconfigured → Fix CORS headers
- Firewall blocking → Check network settings

## Integration Points

### Works With
- frontend-ui-dashboard agent
- auth-security-validator agent
- api-contract-validation skill
- error-normalization-handling skill

### Validates
- API client configuration
- Authentication flow
- Error handling
- Network communication

### Provides
- Integration health report
- Connectivity risk assessment
- Configuration recommendations
- Error handling improvements

## Success Metrics
- **API Base URL:** 100% use environment variables
- **JWT Attachment:** 100% protected endpoints send token
- **Error Handling:** 100% requests have try-catch
- **CORS Errors:** 0 in production
- **Network Failures:** 100% handled gracefully
