ENVIRONMENTS = {
    'dev': {
        'env_prefix': 'tbdd',
        'service_account_suffix': 'n',
        'env_suffix': '_dev',
        'schemas': ['_ing', '_trn'],
        'dev_role': 'dvpr',
    },
    'qa': {
        'env_prefix': 'tbdq',
        'service_account_suffix': 'n',
        'env_suffix': '_qa',
        'schemas': ['_ing', '_trn'],
        'dev_role': 'qa-supp',
    },
    'prod': {
        'env_prefix': 'tbdp',
        'service_account_suffix': 'p',
        'env_suffix': '_prod',
        'schemas': ['_ing', '_trn'],
        'dev_role': 'prod-supp',
    },
}
