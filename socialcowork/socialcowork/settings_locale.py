import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True
IS_LOCAL = True

STATICFILES_DIRS = [
	'/Users/riccardo/Desktop/Progetti/socialcowork/static',
]

MEDIA_ROOT = "/Users/riccardo/Desktop/Progetti/socialcowork/media" 


DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

LOGGING = {
	'version': 1,
	'formatters': {
		'verbose': {
			'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
		},
		'simple': {
			'format': '%(levelname)s %(message)s'
		},
	},
	'filters': {
		'special': {
			'()': 'django.utils.log.RequireDebugFalse',
		},
	},
	'handlers': {
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'verbose'
		},
		'mail_admins': {
			'level': 'ERROR',
			'class': 'django.utils.log.AdminEmailHandler',
			'include_html': True,
			'filters': ['special']
		},
		'debug_file': {
			'level': 'DEBUG',
			'class': 'logging.FileHandler',
			'filename': '/Users/riccardo/Desktop/Progetti/socialcowork/logs/debug.log',
			'formatter': 'verbose'
		},
		'error_file': {
			'level': 'ERROR',
			'class': 'logging.FileHandler',
			'filename': '/Users/riccardo/Desktop/Progetti/socialcowork/logs/error.log',
			'formatter': 'verbose'
		},
	},
	'loggers': {
		'django': {
			'handlers': ['debug_file', 'error_file', 'mail_admins'],
			'level': 'DEBUG',
			'propagate': True,
		},
	}
}