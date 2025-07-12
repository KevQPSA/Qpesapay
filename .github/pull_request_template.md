# QPesaPay Pull Request

## 📋 Description
<!-- Provide a clear and concise description of what this PR does -->

### Type of Change
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🔧 Configuration change
- [ ] 🧪 Test addition/modification
- [ ] 🔒 Security improvement
- [ ] 💰 Financial logic change (requires extra scrutiny)

## 🔗 Related Issues
<!-- Link to related issues using "Fixes #123" or "Closes #123" -->
- Fixes #
- Related to #

## 🧪 Testing
<!-- Describe the tests you ran and how to reproduce them -->

### Test Coverage
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] Security testing performed (if applicable)

### Test Commands
```bash
# Commands to run tests
cd backend
pytest app/tests/ -v
```

## 🔒 Security Checklist
<!-- For financial applications, security is paramount -->

- [ ] No hardcoded secrets or credentials
- [ ] Input validation implemented
- [ ] SQL injection prevention verified
- [ ] Authentication/authorization checked
- [ ] Rate limiting considered
- [ ] Audit logging implemented (for financial operations)
- [ ] Error handling doesn't leak sensitive information

## 💰 Financial Impact Assessment
<!-- Required for changes affecting financial operations -->

- [ ] No impact on financial calculations
- [ ] Decimal precision maintained (no float usage)
- [ ] Transaction integrity preserved
- [ ] Settlement logic verified
- [ ] Exchange rate handling correct
- [ ] Fee calculations accurate

## 📱 M-Pesa/Blockchain Impact
<!-- For changes affecting external integrations -->

- [ ] M-Pesa integration not affected
- [ ] Blockchain transaction logic verified
- [ ] Webhook handling maintained
- [ ] Gas fee calculations correct
- [ ] Network selection logic preserved

## 🚀 Deployment Notes
<!-- Any special deployment considerations -->

- [ ] Database migrations included
- [ ] Environment variables updated
- [ ] Configuration changes documented
- [ ] Backward compatibility maintained
- [ ] Rollback plan available

## 📸 Screenshots/Recordings
<!-- For UI changes, include screenshots or recordings -->

## 📝 Additional Notes
<!-- Any additional information that reviewers should know -->

## ✅ Reviewer Checklist
<!-- For reviewers to complete -->

### Code Quality
- [ ] Code follows project style guidelines
- [ ] Functions are properly documented
- [ ] Error handling is appropriate
- [ ] Performance impact is acceptable

### Security Review
- [ ] Security implications assessed
- [ ] No sensitive data exposed
- [ ] Authentication/authorization correct
- [ ] Input validation sufficient

### Financial Review (if applicable)
- [ ] Financial calculations verified
- [ ] Decimal precision maintained
- [ ] Transaction integrity preserved
- [ ] Audit trail maintained

### Testing Review
- [ ] Test coverage is adequate
- [ ] Tests are meaningful and comprehensive
- [ ] Edge cases are covered
- [ ] Integration tests pass

---

**⚠️ Important**: For financial applications, all changes must be thoroughly reviewed and tested before merging. When in doubt, request additional reviews from domain experts.
