<h1 align="center">Welcome to wresume 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.0.1-blue.svg?cacheSeconds=2592000" />
  <a href="https://twitter.com/NFiiz">
    <img alt="Twitter: NFiiz" src="https://img.shields.io/twitter/follow/NFiiz.svg?style=social" target="_blank" />
  </a>
</p>

> A platform to create and manage a presentable resume

## Install

```sh
pip install -r requirements.txt
python manage.py migrate_schemas
python manage.py create_defaults
python manage.py load_default_templates
python manage.py load_blog_templates
```
The create defaults command creates the public schema and then creates a default admin user.
With credentials `admin | 48sfNdfd4NnU?49$*(9`

Generate a Database dump/backup by running `python manage.py dump_db` on the server and go then to download it from admin at `/mumu`,
that's the admin home

## Author

👤 **Damilola Nifemi Adeyemi**

* Twitter: [@NFiiz](https://twitter.com/NFiiz)
* Github: [@damey2011](https://github.com/damey2011)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_