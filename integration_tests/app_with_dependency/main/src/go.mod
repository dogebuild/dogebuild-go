module su0.io/dogebuild-go/app_with_dependency/main

go 1.14

require github.com/google/go-cmp v0.5.0
replace su0.io/dogebuild-go/app_with_dependency/dependency => /home/su0/git/dogebuild/dogebuild-go/integration_tests/app_with_dependency/dependency/build/src/su0.io/dogebuild-go/app_with_dependency/dependency
