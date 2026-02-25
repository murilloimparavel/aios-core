# 🔐 Security Gate Testing Guide

**Purpose:** Demonstrate how the secret detection gate works and validate its effectiveness.

---

## Test 1: Undetected Secret Pattern (Gate Should Block)

### Setup: Try to commit a file with exposed secret

```bash
# Navigate to the submodule
cd squads/squad-creator-pro-private

# Create a test file with fake API key
cat > test-secrets.env << 'EOF'
# DO NOT COMMIT - Test file for security gate validation
OPENAI_API_KEY=sk-proj-AbCdEfGhIjKlMnOpQrStUvWxYz1234567890
DATABASE_PASSWORD=MySecurePassword123!
AWS_ACCESS_KEY=AKIA3BCD5E7F9H1J3K5L
EOF

# Try to add and commit
git add test-secrets.env
git commit -m "test: add secrets file (will be blocked by gate)"

# Try to push - THIS WILL BE BLOCKED
git push origin main
```

### Expected Result

❌ **Push BLOCKED** - GitHub Actions security gate prevents merge

```
❌ SECURITY ALERT: Secrets detected in this commit!

Detected potential secrets:
- API Keys (sk-proj-* pattern)
- Passwords (MySecurePassword123!)
- AWS Access Keys (AKIA*)

❗ This PR/push is BLOCKED due to security concerns.
Please remove all secrets and try again.
```

### Remediation Steps

```bash
# Remove the secret file
git rm test-secrets.env

# Commit the removal
git commit -m "fix: remove test secrets file"

# Now push will succeed
git push origin main
```

---

## Test 2: Valid Configuration (Gate Should Pass)

### Setup: Properly use .env pattern

```bash
cd squads/squad-creator-pro-private

# Copy template
cp .env.example .env

# Edit .env (it's in .gitignore, won't be committed)
echo "OPENAI_API_KEY=sk-test-key-here" > .env

# Create a legitimate code change
cat > new-feature.js << 'EOF'
// Load config from .env (not hardcoding)
require('dotenv').config();

const apiKey = process.env.OPENAI_API_KEY;
console.log('Using configured API key');
EOF

# Commit the code (not .env)
git add new-feature.js
git commit -m "feat: add new feature using env variables"

# Push - THIS WILL SUCCEED
git push origin main
```

### Expected Result

✅ **Push SUCCESS** - Security gate passes

```
✅ Secret Detection Gate: PASSED - No secrets detected
✅ .gitignore Check: PASSED
✅ File Extension Check: PASSED
✅ Pattern Regex Check: PASSED

✅ **SECURITY GATE PASSED** - No secrets detected
```

---

## Test 3: Suspicious File Extensions (Gate Should Block)

### Setup: Try to commit a .pem file

```bash
cd squads/squad-creator-pro-private

# Create a fake private key file
openssl genrsa -out test-key.pem 2048

# Try to commit it
git add test-key.pem
git commit -m "test: add test private key"

# Try to push - WILL BE BLOCKED
git push origin main
```

### Expected Result

❌ **Push BLOCKED** - File extension check prevents dangerous files

```
❌ SECURITY ALERT: Suspicious files found!
These files should NOT be committed:
./test-key.pem

The gate detected dangerous file types:
- .pem files (private keys)
- .key files (encryption keys)
- .jks files (Java keystores)
- .p12 files (PKCS#12 certificates)
```

### Remediation

```bash
# Remove the key file
git rm test-key.pem

# Add to .gitignore if needed
echo "test-key.pem" >> .gitignore

# Commit
git commit -m "fix: remove private key file"

# Push will now succeed
git push origin main
```

---

## Test 4: Hardcoded Password Pattern (Gate Should Block)

### Setup: Hardcoded credentials in code

```bash
cd squads/squad-creator-pro-private

# Create a file with hardcoded password
cat > bad-auth.js << 'EOF'
// ❌ BAD: Hardcoded password (will be blocked)
const dbPassword = "password123!secure";
const apiKey = "sk-ABCDEFGHIJKLMNOPQRSTUVWxyz";
const credentials = {
  user: "admin",
  password: "admin123"
};
EOF

# Try to commit
git add bad-auth.js
git commit -m "feat: add authentication (with hardcoded creds)"

# Try to push - WILL BE BLOCKED
git push origin main
```

### Expected Result

❌ **Push BLOCKED** - Regex pattern detection finds hardcoded credentials

```
❌ SECURITY ALERT: Secret patterns detected!

Detected patterns:
- password assignment with strong value
- sk-* API key pattern
- AWS/GCP credential patterns

❗ This PR/push is BLOCKED due to security concerns.
```

### Correct Approach

```bash
# ✅ CORRECT: Use environment variables
cat > auth.js << 'EOF'
// ✅ GOOD: Use environment variables
const dbPassword = process.env.DB_PASSWORD;
const apiKey = process.env.OPENAI_API_KEY;
const credentials = {
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD
};
EOF

# Commit the corrected code
git rm bad-auth.js
git add auth.js
git commit -m "fix: use environment variables for credentials"

# Push will succeed
git push origin main
```

---

## Test 5: AWS Credential Detection (Gate Should Block)

### Setup: Exposed AWS keys

```bash
cd squads/squad-creator-pro-private

# Create a config file with AWS credentials
cat > aws-config.json << 'EOF'
{
  "aws_access_key_id": "AKIA3BCD5E7F9H1J3K5L",
  "aws_secret_access_key": "wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY"
}
EOF

# Try to commit
git add aws-config.json
git commit -m "config: add AWS credentials"

# Try to push - WILL BE BLOCKED
git push origin main
```

### Expected Result

❌ **Push BLOCKED** - AWS pattern detection (AKIA*)

```
❌ SECURITY ALERT: Found potential AWS access key

The gate detected AWS credentials patterns:
- AKIA* (AWS Access Key ID pattern)

❗ This PR/push is BLOCKED due to security concerns.
```

---

## Test 6: GitHub Actions Workflow Validation

### Check Workflow Runs Automatically

```bash
# Create a PR with your test changes
git checkout -b test-security-gate
echo "test" > test.txt
git add test.txt
git commit -m "test: validation"
git push origin test-security-gate

# Create PR via GitHub
gh pr create --title "Test: Security Gate" --body "Testing security gate"

# GitHub Actions will automatically:
# 1. Run TruffleHog scanner
# 2. Check .gitignore compliance
# 3. Validate file extensions
# 4. Run regex pattern scans
# 5. Post results as comment

# Check workflow results
gh pr view --json checks
```

### Monitor Workflow Status

Visit: `https://github.com/murilloimparavel/squads-mvp/actions`

You'll see:
- ✅ Secret Detection Gate
- ✅ .gitignore Compliance
- ✅ File Extension Check
- ✅ Pattern Regex Check
- ✅ Security Gate Summary

---

## Real-World Scenarios

### Scenario A: Developer Accidentally Commits .env

```bash
# Developer creates .env with real credentials
echo "OPENAI_API_KEY=sk-abc123..." > .env

# Try to commit everything
git add .
git commit -m "feat: add feature"

# Result: .env is NOT committed (already in .gitignore)
# Only actual code changes committed
git status  # .env not shown
```

### Scenario B: Leaked Secret in Git History

```bash
# If secret was already pushed to origin:

# 1. Immediately rotate the credential
gh secret set OPENAI_API_KEY --body "sk-new-key"

# 2. Remove from git history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env' -- --all

# 3. Force push
git push origin --force-with-lease --all

# 4. Notify team about rotation
```

### Scenario C: PR with Security Issues

```bash
# Reviewer sees security gate failed
# GitHub Actions comment shows:
❌ SECURITY GATE FAILED - Secrets detected

# PR author must:
# 1. Remove the exposed secrets
# 2. Push a new commit
# 3. Gate will re-run automatically
# 4. Once passing, can merge
```

---

## Workflow Files Reference

**Location:** `.github/workflows/secret-gate.yml`

**Triggers:**
- On every `git push`
- On every PR (opened, synchronized, reopened)

**Jobs:**
1. `detect-secrets` - TruffleHog scanning
2. `gitignore-check` - Compliance validation
3. `file-extension-check` - Dangerous file types
4. `regex-pattern-check` - Pattern-based detection
5. `summary` - Reports results

---

## Quick Reference: Commands to Test

```bash
# Setup
cd squads/squad-creator-pro-private
cp .env.example .env
nano .env  # Add your test values

# Test 1: Safe commit (should pass)
echo "# comment" > safe-code.js
git add safe-code.js
git commit -m "test: safe code"
git push origin main  # ✅ PASS

# Test 2: Unsafe commit (should fail)
echo "API_KEY=sk-test123" > unsafe.txt
git add unsafe.txt
git commit -m "test: with secret"
git push origin main  # ❌ BLOCK - Remove file

# Test 3: Check gate status
gh pr view <pr-number> --json checks

# Test 4: Cleanup
git reset HEAD~1
git rm unsafe.txt
git commit -m "fix: remove secret"
```

---

## Troubleshooting

### Gate Passes But Shouldn't Have

```bash
# Check TruffleHog version
~/.local/bin/coderabbit --version

# Run TruffleHog manually
trufflehog git file:// --json
```

### False Positives

If you have legitimate content that matches patterns:

1. Document in `.env.example`
2. Add to ignored patterns (if appropriate)
3. Use code comments to explain why it's safe:

```javascript
// Safe example - not a real credential
const example = "sk-test-in-documentation";
```

---

## Success Criteria

✅ **Gate is working when:**

1. Files with `.env` extension cannot be committed
2. Files with `.pem`, `.key`, `.jks` extensions are blocked
3. API key patterns (`sk-*`, `AKIA*`) are detected
4. Database password patterns are caught
5. Token patterns are identified
6. Manual `.env` files work (because in .gitignore)
7. PRs show security gate status
8. Error messages are helpful and actionable

---

**Remember:** The security gate is your safety net. Use it to learn, not fear. ✅

