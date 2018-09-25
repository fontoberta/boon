docker-compose up -d
sleep 30
docker-compose run --rm web python3 manage.py migrate
docker-compose run --rm web python3 manage.py loaddata fixtures/fixture.json
docker-compose run --rm web cp -R fixtures/images/fontoberta  media/
docker-compose run --rm web cp -R fixtures/images/photography  media/
docker-compose run --rm web python3 manage.py collectstatic --noinput