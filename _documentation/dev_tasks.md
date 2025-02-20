<!-- _documentation/dev_tasks.md -->
# Backlogger Development Tasks

## Phase 1: Core Infrastructure (Sprint 1-2)

### Project Configuration
- [x] Set up project requirements [HIGH]
  - [x] Create requirements directory structure
  - [x] Set up base.txt with core dependencies
  - [x] Set up development.txt with testing dependencies
  - [x] Set up production.txt with deployment dependencies
  - [x] Install development requirements
- [x] Set up proper .env usage [HIGH]
  - [x] Install python-dotenv
  - [x] Configure .env loading in settings/base.py
  - [x] Update settings to use environment variables
- [x] Restructure Django settings
  - [x] Split settings into base/development/production
  - [x] Configure environment-specific settings
  - [x] Configure CORS and security headers
  
### Authentications & Security Foundation
- [x] Create base user serializer
- [x] Create registration serializer
- [x] Add password validation rules
- [x] Implement email format validation
- [x] Add custom validation methods
- [x] Create registration view
- [x] Implement rate limiting
- [x] Create consolidated security headers
- [x] Configure basic JWT settings
- [ ] Implement API Authentications [HIGH]
  - [ ] Create login view for JWT token generation
  - [ ] Create token refresh view
  - [ ] Add token blacklist functionality
  - [ ] Implement protected view decorators
- [ ] Add Authentications Tests [HIGH]
  - [ ] Test login flow
  - [ ] Test token refresh
  - [ ] Test token blacklist
  - [ ] Test protected views

### Core Data Models
- [x] Create Organisation model [HIGH]
  - [x] Core identification (UUID, name)
  - [x] Status and subscription tier enums
  - [x] Access control fields
  - [x] Hierarchy configuration
  - [x] Billing and subscription tracking
  - [x] Compliance and audit fields
  - [x] Business rule validation
- [x] Create Subscription model [HIGH]
  - [x] Implement billing intervals
  - [x] Add usage tracking
  - [x] Set up validation rules
  - [x] Create tier-based limits
- [ ] Create Item model [HIGH]
  - [ ] Implement NodeType enumeration
    - [ ] Create base node types (Task, Bug, Improvement)
    - [ ] Add Pro tier types (Feature, Epic, User Story, Technical Items)
    - [ ] Add Business tier types (Waterfall phases, Business Items)
  - [ ] Set up composite keys with organisation
  - [ ] Implement hierarchy validation rules
    - [ ] Validate methodology-specific hierarchies (Kanban, Scrum, Waterfall)
    - [ ] Implement tier-based hierarchy restrictions
    - [ ] Add methodology switching validation
  - [ ] Create migration files
  - [ ] Add hierarchy depth validation
    - [ ] Implement tier-specific depth limits
    - [ ] Add methodology-specific depth validation
    - [ ] Create custom depth validators by item type
  - [ ] Implement parent-child relationship logic
    - [ ] Add methodology-specific relationship rules
    - [ ] Implement tier-based relationship restrictions
    - [ ] Create cross-methodology relationship validation
  - [ ] Set up item state tracking
    - [ ] Add basic state machine for all items
    - [ ] Create methodology-specific state flows
    - [ ] Implement state transition validation
  - [ ] Add subscription tier constraints
    - [ ] Implement Starter tier limitations
    - [ ] Add Pro tier feature access
    - [ ] Create Business tier capabilities
  - [ ] Create custom indexes for hierarchy queries
    - [ ] Add indexes for parent-child queries
    - [ ] Create methodology-specific indexes
    - [ ] Implement cross-project relationship indexes
  - [ ] Implement soft delete functionality
    - [ ] Add cascade soft delete for hierarchies
    - [ ] Create reactivation logic
    - [ ] Implement tier-specific retention rules
  - [ ] Add methodology mapping support [HIGH]
    - [ ] Implement Kanban flow-based structure
    - [ ] Create Scrum iterative hierarchy
    - [ ] Add Waterfall phase-based organization
    - [ ] Support methodology switching
  - [ ] Create tier-based access control [HIGH]
    - [ ] Implement Starter tier restrictions
    - [ ] Add Pro tier feature gates
    - [ ] Create Business tier capabilities
  
## Phase 2: Basic Functionality (Sprint 3-4)

### Email System
- [ ] Implement email verification flow [HIGH]
- [ ] Add resend verification endpoint [MEDIUM]
- [ ] Create password reset views [HIGH]
- [ ] Create email preview URL patterns [MEDIUM]
- [ ] Implement preview view [MEDIUM]

### API Serializers
- [ ] Create base Item serializer [HIGH]
  - [ ] Implement type-specific field handling
  - [ ] Add hierarchy validation
  - [ ] Create organisation relationship handling
- [ ] Create Organisation serializer [HIGH]
- [ ] Create Subscription serializer [HIGH]
  
### Basic API Endpoints
- [ ] Create Item endpoints [HIGH]
  - [ ] Implement CRUD operations
  - [ ] Add filtering by node_type
  - [ ] Add hierarchy traversal endpoints
- [ ] Create Organisation endpoints [HIGH]
- [ ] Create Subscription endpoints [HIGH]

### Testing Infrastructure
- [x] Set up pytest configuration [HIGH]
  - [x] Configure pytest.ini with test settings
  - [x] Set up conftest.py with shared fixtures
  - [x] Configure test database settings
  - [x] Set up coverage reporting
- [ ] Create test directory structure [HIGH]
  - [x] Set up unit test directory
  - [x] Create integration test directory
  - [x] Establish e2e test directory
  - [x] Set up fixtures directory
- [ ] Set up test fixtures [HIGH]
  - [x] Create base test data fixtures
  - [ ] Implement factory_boy factories
  - [x] Set up authentications fixtures
  - [x] Create shared test utilities
- [x] Set up test factories infrastructure [HIGH]
  - [x] Rename /test/fixtures/factories.py to authentication.py
  - [x] Create /tests/factories folder
  - [x] Create __init__.py file 
  - [x] Edit __init__.py to expose the UserFactory
- [ ] Implement CI/CD test integration [HIGH]
  - [ ] Set up GitHub Actions for testing
  - [ ] Configure test automation
  - [ ] Set up test reporting
  - [ ] Implement test coverage checks


## Phase 3: Team & Access Control (Sprint 5-6)

### Team Management
- [ ] Create Team model [HIGH]
  - [ ] Add organisation relationship
  - [ ] Implement subscription limits
- [ ] Implement team membership model [HIGH]
- [ ] Create team serializers [HIGH]
- [ ] Add team views [HIGH]
- [ ] Implement team permissions [HIGH]

### Access Control
- [ ] Create role hierarchy [HIGH]
- [ ] Implement permission models [HIGH]
- [ ] Add subscription limits [MEDIUM]
- [ ] Create access control decorators [HIGH]

### Subscription Management
- [ ] Create subscription model [MEDIUM]
- [ ] Implement usage tracking [MEDIUM]
- [ ] Add limit enforcement [MEDIUM]
- [ ] Create upgrade/downgrade logic [LOW]

## Phase 4: Change Impact Analysis (Sprint 7-8)

### Core Implementation
- [ ] Create ChangeRequest model [HIGH]
- [ ] Implement Impact model [HIGH]
- [ ] Create StakeholderImpact model [HIGH]
- [ ] Implement TeamImpact model [HIGH]
- [ ] Add relationship tracking [HIGH]

### Analysis Features
- [ ] Implement cost calculation [MEDIUM]
- [ ] Create dependency tracker [MEDIUM]
- [ ] Add impact scoring [MEDIUM]
- [ ] Implement risk assessment [MEDIUM]
- [ ] Create notification system [HIGH]

## Phase 5: Advanced Features (Sprint 9-10)

### Email Features
- [ ] Create tracking pixel system [LOW]
- [ ] Implement open tracking [LOW]
- [ ] Add click tracking [LOW]
- [ ] Create tracking data models [LOW]
- [ ] Add email client simulation [LOW]

### Advanced API Features
- [ ] Add versioning support [MEDIUM]
- [ ] Create bulk operations [MEDIUM]
- [ ] Implement filtering [HIGH]
- [ ] Add export functionality [MEDIUM]
- [ ] Implement webhook system [LOW]

## Continuous Testing (All Phases)

### Unit Testing (/tests/unit/)
- [ ] Model Test Suites [HIGH]
  - [ ] Organisation Model Tests
    - [ ] Test tier-based feature enablement
    - [ ] Test domain validation for Enterprise tier
    - [ ] Test storage limit calculations
    - [ ] Test hierarchy enablement rules
    - [ ] Test business rule validation
    - [ ] Test role hierarchy JSON validation
    - [ ] Test audit log tracking
    - [ ] Test GDPR compliance settings
  - [ ] Subscription Model Tests
    - [ ] Test billing interval logic
    - [ ] Test usage tracking calculations
    - [ ] Test tier-based limits
    - [ ] Test trial period handling
    - [ ] Test subscription status transitions
    - [ ] Test period validation rules
    - [ ] Test max user/storage calculations
  - [ ] Item Model Tests
    - [ ] Test hierarchy validation rules
    - [ ] Test parent-child relationships
    - [ ] Test subscription tier constraints
    - [ ] Test composite key uniqueness
    - [ ] Test soft delete behavior
    - [ ] Test hierarchy depth validation
    - [ ] Test node type validation
- [x] Implement serializer tests (in test_serializers.py) [HIGH]
  - [x] Test serializer functionality
  - [x] Add validation tests with parameterized tests
  - [x] Test required fiields
  - [x] Test data validation
- [ ] Create view test suite [HIGH]
  - [ ] Test CRUD operations
  - [ ] Implement permission tests
  - [ ] Add authentications tests
  - [ ] Create error handling tests
- [x] Template tests (in test_templates) [MEDIUM]
  - [x] Test email templates
  - [x] Validate template rendering
  - [x] Test template context
  - [x] Test template styling
  - [x] Test missing variable handling
- [ ] Validator tests (in test_validators.py) [HIGH]
  - [x] Test field validators
  - [x] Implement custom validation rules
  - [x] Test validation messages
  - [x] Test validator help text
  - [x] Test all password validators
    - [x] SpecialCharacterValidator
    - [x] UppercaseValidator
    - [x] Lowercase Validator
    - [x] NumberValidator
    - [x] RepeatedCharacterValidator
    - [x] MaxLengthValidator

## Integration Testing (/tests/integration/)
- [x] Create authentications integration tests [HIGH]
- [x] Test registration flow (test_registration.py)
  - [x] Complete registration flow testing
  - [x] Email validation checks
  - [x] Duplicate registration testing
  - [x] Password validation
  - [x] Template variables testing
- [x] Implement validation tests
  - [x] Email format validation
  - [x] Password validation rules
  - [x] Existing user/email check
  - [x] Empty field handling
- [x] Create verification tests
  - [x] Successful verification flow
  - [x] Invalid token handling
  - [x] Expired link testing
  - [x] Already verified user check
  - [x] Wrong user verification attempt tests
- [ ] Create API integration tests [HIGH]
  - [ ] Test API endpoints
  - [ ] Implement workflow tests
  - [ ] Add performance benchmarks
  - [ ] Test API versioning
- [ ]  Add service integration tests [HIGH]
  - [ ] Test external service integration
  - [ ] Create mock service tests
  - [ ] Add error handling tests
  - [ ] Implement timeout tests
- [ ] Create Organisation/Subscription Integration Tests [HIGH]
  - [ ] Test tier upgrade/downgrade flows
  - [ ] Test usage limit enforcement
  - [ ] Test feature access by tier
  - [ ] Test billing interval changes
  - [ ] Test organisation state transitions
  - [ ] Test subscription renewal flows
  
### E2E Testing (/tests/e2e/)
- [ ] Set up end-to-end test framework [HIGH]
  - [ ] Configure e2e test environment
  - [ ] Set up test data seeding
  - [ ] Create test user journeys
- [ ] Implement authentications e2e tests [HIGH]
  - [ ] Test complete registration flow
  - [ ] Test login/logout process
  - [ ] Test password reset flow
- [ ] Create workflow e2e tests [HIGH]
  - [ ] Test main user workflows
  - [ ] Implement cross-feature tests
  - [ ] Test error scenarios
- [ ] Create Organisation E2E Tests [HIGH]
  - [ ] Test complete organisation creation flow
  - [ ] Test subscription management workflow
  - [ ] Test tier change scenarios
  - [ ] Test member invitation flow
  - [ ] Test domain restriction enforcement

### Test Fixtures (/tests/fixtures/)
- [ ] Create base test data [HIGH]
  - [ ] Implement test data factories
  - [ ] Create authentications fixtures
  - [ ] Set up shared test utilities
- [ ] Add factory boy implementations [HIGH]
  - [ ] Create model factories
  - [ ] Implement related factories
  - [ ] Add factory sequences
- [ ] Create mock data generators [MEDIUM]
  - [ ] Implement mock service responses
  - [ ] Create mock API data
  - [ ] Set up mock configurations
- [x] Add Organisation/Subscription Factories [HIGH]
  - [x] Create OrganisationFactory with tier variants
  - [x] Create SubscriptionFactory with status variants
  - [x] Set up related fixture factories
  - [x] Create test data generators for usage metrics

## Documentation (All Phases)

### Technical Documentation
- [ ] Create API documentation [HIGH]
- [ ] Document data models [HIGH]
- [ ] Create email template guide [MEDIUM]
- [ ] Document testing procedures [HIGH]

### Deployment Documentation
- [ ] Create unified deployment guide [HIGH]
- [ ] Write monitoring documentation [MEDIUM]
- [ ] Add troubleshooting guide [MEDIUM]

## Required Dependencies

```python
# requirements.txt
# Core & Authentications
djangorestframework==3.15.2
djangorestframework-jwt==2.0.0
django-cors-headers==4.3.0
django-guardian==2.4.0
django-filter==23.5
django-versioning==1.0.0

# Email Processing
premailer==3.10.0
email-validator==2.0.0
django-html-sanitizer==0.1.5

# Testing
pytest-django==4.5.2
pytest-cov==4.1.0
pytest-xdist==3.3.1
locust==2.15.1
```

## Development Setup

```bash
# Initial setup
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initial_data

# Running tests
pytest
pytest apps/authentications/tests/
pytest apps/hierarchy/tests/
```

## Configuration

```python
# settings/base.py
API_SETTINGS = {
    'VERSION': 'v1',
    'HIERARCHY_MAX_DEPTH': 6,
    'ENABLE_VERSIONING': True,
    'TRACK_CHANGES': True,
    'RATE_LIMIT': '100/hour'
}

EMAIL_SETTINGS = {
    'TRACKING_ENABLED': True,
    'PREVIEW_ENABLED': True,
    'AUTH_REQUIRED': True
}
```