# Run this with: 'source ./scripts/setup-local-dev.fish'

set -gx APP_SETTINGS server.config.DevelopmentConfig
set -gx DATABASE_URL postgres://postgres:postgres@localhost:5432/users_dev
set -gx DATABASE_TEST_URL postgres://postgres:postgres@localhost:5432/users_test
set -gx SECRET_KEY my_precious
