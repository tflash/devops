# Terraform tips & tricks

1. Need import module to remote state. Need added to module construction single quote
 terragrunt import 'module.cdn.aws_cloudfront_origin_access_identity.this["identity"]' ID

2. Need import module contains helm_release
   See helm list
   NAME   	NAMESPACE	REVISION	UPDATED         STATUS  	CHART        	APP VERSION
   traefik	traefik  	2       	-	              deployed	traefik       1.0.2	1.0.2

terraform import  module.traefik.helm_release.traefik traefik/traefik
