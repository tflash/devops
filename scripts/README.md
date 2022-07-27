# Terraform tips & tricks

1. Need import module to remote state. Need added to module construction single quote
 terragrunt import 'module.cdn.aws_cloudfront_origin_access_identity.this["identity"]' EWWLC0G8QQN7I   
