SECURITY_DOMAINS = {
    'security_domains': {
        'product': {
            'domains': {
                'widget': {
                    'subdomains': {
                        'master': {
                            'security_groups': [
                                'widget-master-data',
                                'widget-master-data-sensitive',
                            ]
                        },
                        'sales': {
                            'security_groups': [
                                'widget-sales-actuals',
                                'widget-sales-forecast',
                            ],
                            'subdomains': {
                                'new_widget_sales': {
                                    'subdomains': {
                                        'aggregated': {
                                            'subdomains': {
                                                'actuals': {
                                                    'security_groups': [
                                                        'widget-sales-new-aggregated-actuals'
                                                    ]
                                                }
                                            }
                                        },
                                        'used_widget_sales': {
                                            'subdomains': {
                                                'vin_based': {
                                                    'sudbomains': {
                                                        'actuals': {
                                                            'security_groups': [
                                                                'vehicle-sales-used-car-vin-based-actuals'
                                                            ]
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                    },
                                },
                                'pricing': {
                                    'security_groups': [
                                        'widget-pricing',
                                        'widget-pricing-sensitive',
                                    ]
                                },
                                'configuration': {
                                    'security_groups': [
                                        'widget-configuration',
                                        'widget-configuration-sensitive',
                                    ]
                                },
                                'inventory_volume': {
                                    'security_groups': [
                                        'widget-inventory-volume',
                                        'widget-inventory-volume-sensitive',
                                    ]
                                },
                                'orders': {
                                    'subdomains': {
                                        'forecast': {'security_groups': ['widget-orders-actuals']},
                                        'actuals': {'security_groups': ['widget-orders-actuals']},
                                    }
                                },
                                'quality': {
                                    'subdomains': {
                                        'reports': {'security_groups': ['quality-reports']},
                                    }
                                },
                            },
                        },
                        'production': {
                            'domains': {
                                'manufacturing': {
                                    'subdomains': {
                                        'defects': {'security_groups': ['manufacturing-defects']},
                                        'productivity': {
                                            'security_groups': ['manufacturing-productivity']
                                        },
                                        'job_process': {
                                            'security_groups': ['manufacturing-job-process']
                                        },
                                        'equipment': {
                                            'security_groups': ['manufacturing-equipment']
                                        },
                                        'inspection': {
                                            'security_groups': ['manufacturing-inspection']
                                        },
                                    }
                                }
                            }
                        },
                    }
                },
                'api': {
                    'subdomains': {
                        'master': {
                            'security_groups': [
                                'api-master-data',
                                'api-master-data-sensitive',
                            ]
                        },
                    }
                },
                'accounting': {
                    'subdomains': {
                        'master': {
                            'security_groups': [
                                'accounting-master-data',
                                'accounting-master-data-sensitive',
                            ]
                        },
                    },
                },
            }
        },
    },
}
