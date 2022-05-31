ENVIRONMENTS = {
    'dev': {
        'env_prefix': 'dev',
        'service_account_suffix': 'dev',
        'env_suffix': '_dev',
        'sensitive_suffix': 'sensitive',
        'schemas': ['_ingest', '_transform'],
        'support_role': 'dev-support',
    },
    'test': {
        'env_prefix': 'test',
        'service_account_suffix': 'test',
        'env_suffix': '_qa',
        'sensitive_suffix': 'sensitive',
        'schemas': ['_ingest', '_transform'],
        'support_role': 'test-suuport',
    },
    'prod': {
        'env_prefix': 'prod',
        'service_account_suffix': 'prod',
        'env_suffix': '_prod',
        'sensitive_suffix': 'sensitive',
        'schemas': ['_ingest', '_transform'],
        'support_role': 'prod-support',
    },
}
