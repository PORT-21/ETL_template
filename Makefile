redis_extractor_out_shell:
	docker-compose exec extractor_to_transformer redis-cli

redis_transformer_out_shell:
	docker-compose exec transformer_to_loader redis-cli
