# deploy-chroma

## About

Source & config for chroma deployment on VESSL Service with credential.

## Local test

1. Install dependencies

```sh
poetry install
```

2. Build credential info: currently support only one user-pwd pair

```sh
poetry run ./prepare-auth.sh <username> <password>
```

of you can set `CHROMA_SERVER_AUTHN_USERNAME` `CHROMA_SERVER_AUTHN_PASSWORD` envvar before run the script.

```sh
export CHROMA_SERVER_AUTHN_USERNAME=username
export CHROMA_SERVER_AUTHN_PASSWORD=password
poetry run ./prepare-auth.sh
```

3. Run chroma instance

```sh
poetry run ./launch-chroma.sh
```

4. Test with auth

Change `admin:admin` part of `test-auth.py` and run the following

```sh
poetry run ./test-auth.py
```

## Deploying to VESSL Service

1. Follow the VESSL Service guide for bootstraping the [VESSL Docs](https://docs.vessl.ai/guides/serve/create-a-service)

2. Update the credential envvars of `CHROMA_SERVER_AUTHN_USERNAME` `CHROMA_SERVER_AUTHN_PASSWORD` in `service.yaml`

3. Use the yaml file to launch a VESSL Service revision.

4. Test using `test-auth.py` bu using with endpoint of VESSL Service.
