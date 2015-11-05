.PHONY: docker-compose

docker-compose:
	docker-compose up

pushup:
	test -z "`git status -s`"
	git push --all
	git push origin --tags
	git checkout develop
	git merge master
