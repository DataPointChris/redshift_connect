SECURITY_DOMAINS = {
    'security_domains': {
        'party': {
            'domains': {
                'customer': {
                    'subdomains': {
                        'master': {'security_groups': ['customer-master']},
                        'vehicle_purchase_writeup': {
                            'security_groups': ['customer-vehicle-purchase-writeup']
                        },
                        'call_center': {
                            'security_groups': ['call-center-toy', 'call-center-toy-sen']
                        },
                        'demographics': {'security_groups': ['customer-demographics']},
                        'communication_management': {
                            'security_groups': ['customer-communication-management-sen']
                        },
                        'dealer_relationship': {
                            'security_groups': ['customer-dealer-relationship']
                        },
                        'parts_ecommerce': {
                            'security_groups': ['customer-parts-ecommerce']
                        },
                        'predictive_scores': {
                            'security_groups': [
                                'customer-predictive-score',
                                'customer-predictive-score-toyota',
                                'customer-predictive-score-lexus',
                            ]
                        },
                        'alias': {'security_groups': ['customer-alias']},
                        'social_media': {'security_groups': ['']},
                        'marketing': {'security_groups': ['customer-marketing']},
                    }
                },
                'vendors_partners': {'security_groups': ['party-vendor-partner']},
                'non_customer': {'security_groups': ['non-customer-sensitive']},
                'distribution_region_dealer': {
                    'subdomains': {
                        'dealership_non_dealer_region_master': {
                            'security_groups': ['dealer-master']
                        },
                        'dealership_metrics': {
                            'security_groups': [
                                'party-dealer-management',
                                'party-dealer-management-sensitive',
                            ]
                        },
                        'dealer_personnel': {'security_groups': ['dealer-personnel']},
                        'dealer_call_center': {'security_groups': ['dealer-call-center']},
                        'region_master': {
                            'security_groups': ['party-region-master-sensitive']
                        },
                        'dealer_staff': {'security_groups': ['dealership-staff']},
                    }
                },
            }
        },
        'product': {
            'domains': {
                'vehicle': {
                    'subdomains': {
                        'master': {
                            'security_groups': [
                                'vehicle-master-data',
                                'vehicle-master-data-sensitive',
                                'vehicle-master-data-lexus-sensitive',
                                'vehicle-master-data-toyota-sensitive',
                            ]
                        },
                        'sales': {
                            'security_groups': [
                                'vehicle-sales',
                                'sales-actuals-sen',
                                'sales-forecast',
                                'sales-forecast-factor',
                                'sales-forecast-sen',
                                'vin-dist-sales-sen',
                                'sales-incentives-forecast-sen',
                            ],
                            'subdomains': {
                                'new_car_sales': {
                                    'subdomains': {
                                        'aggregated': {
                                            'subdomains': {
                                                'actuals': {
                                                    'security_groups': [
                                                        'vehicle-sales-new-car-aggregated-actuals'
                                                    ]
                                                }
                                            }
                                        },
                                        'vin_based': {
                                            'subdomains': {
                                                'actuals': {
                                                    'security_groups': [
                                                        'vehicle-sales-new-car-vin-based-actuals'
                                                    ]
                                                }
                                            }
                                        },
                                    }
                                },
                                'used_car_sales': {
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
                        'incentives': {
                            'forecast': {
                                'security_groups': ['vehicle-incentive-forecast']
                            },
                            'actuals': {
                                'security_groups': [
                                    'vehicle-configuration',
                                    'vehicle-configuration-sen',
                                ]
                            },
                        },
                        'pricing': {
                            'security_groups': [
                                'vehicle-pricing',
                                'vehicle-pricing-sensitive',
                            ]
                        },
                        'configuration': {
                            'security_groups': [
                                'vehicle-configuration',
                                'vehicle-configuration-sen',
                            ]
                        },
                        'inventory_volume': {
                            'security_groups': [
                                'vehicle-inventory-volume',
                                'vehicle-inventory-volume-sen',
                            ]
                        },
                        'factors': {'security_groups': ['vehicle-factors-sensitive']},
                        'planning': {'security_groups': ['vehicle-planning-sensitive']},
                        'orders': {
                            'subdomains': {
                                'forecast': {
                                    'security_groups': ['vehicle-orders-actuals']
                                },
                                'actuals': {
                                    'security_groups': ['vehicle-orders-actuals']
                                },
                            }
                        },
                        'logistics_management': {
                            'security_groups': [
                                'vehicle-logistics-management',
                                'vehicle-logistics-mgmt-sensitive',
                            ]
                        },
                    }
                },
                'telematics': {'security_groups': ['telematics']},
                'parts': {
                    'subdomains': {
                        'direct_parts': {
                            'security_groups': ['parts-directparts'],
                            'subdomains': {
                                'manufacturing_parts': {
                                    'security_groups': [
                                        'parts-directparts-manufacturing'
                                    ],
                                    'subdomains': {
                                        'supplier_survey': {
                                            'security_groups': [
                                                'parts-directparts-manufacturing-supplier-survey'
                                            ]
                                        },
                                        'manufacturing_material': {
                                            'security_groups': ['']
                                        },
                                        'inline_accessory_part': {
                                            'security_groups': ['']
                                        },
                                    },
                                },
                            },
                        },
                        'indirect_parts': {
                            'subdomains': {
                                'service_parts': {
                                    'security_groups': [
                                        'parts-indirectparts-serviceparts'
                                    ],
                                    'subdomains': {
                                        'logistics': {'security_groups': ['']},
                                        'procurement': {
                                            'subdomains': {
                                                'parts_distribution_center': {
                                                    'security_groups': ['']
                                                },
                                                'sales': {
                                                    'security_groups': [
                                                        'sales-serviceparts'
                                                    ]
                                                },
                                                'transactions': {
                                                    'security_groups': [
                                                        'parts-transactions'
                                                    ]
                                                },
                                                'incentives': {'security_groups': ['']},
                                                'inventory_management': {
                                                    'security_groups': [
                                                        'parts-pdc-warehouse-management'
                                                    ],
                                                    'subdomains': {
                                                        'supply': {
                                                            'security_groups': [
                                                                'parts-pdc-supply'
                                                            ]
                                                        }
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'accessory_parts': {'security_groups': ['']},
                            }
                        },
                        'logistics_management': {
                            'security_groups': ['parts-logistics-management']
                        },
                    },
                },
                'quality': {
                    'subdomains': {
                        'campaigns': {'security_groups': ['quality-campaigns']},
                        'reports': {'security_groups': ['quality-reports']},
                        'diagnostics': {'security_groups': ['quality-diagnostics']},
                    }
                },
            }
        },
        'cross_domain_business_functions': {
            'domains': {
                'manufacturing': {
                    'subdomains': {
                        'defects': {'security_groups': ['manufacturing-defects']},
                        'productivity': {
                            'security_groups': ['manufacturing-productivity']
                        },
                        'job_process': {'security_groups': ['manufacturing-job-process']},
                        'affiliates': {'security_groups': ['manufacturing-affiliates']},
                        'equipment': {'security_groups': ['manufacturing-equipment']},
                        'inspection': {'security_groups': ['manufacturing-inspection']},
                    }
                },
                'warranty': {
                    'security_groups': ['warranty', 'warranty-sensitive'],
                    'subdomains': {
                        'parts_claims': {'security_groups': ['warranty-partsclaims']},
                        'warranty_insurance': {'security_groups': ['warranty-insurance']},
                    },
                    'service_history': {
                        'security_groups': [
                            'service-history',
                            'toy-service-hist',
                            'lex-service-hist',
                            'lex-service-hist-puertorico',
                            'toy-service-hist-puertorico',
                        ]
                    },
                },
                'accounting': {
                    'subdomains': {
                        'master': {'security_groups': ['accounting-master']},
                        'calendar': {
                            'security_groups': [
                                'accounting-calendar',
                                'accounting-calendar-sensitive',
                            ]
                        },
                        'transactions': {
                            'security_groups': [
                                'accounting-transactions',
                                'accounting-transactions-sensitive',
                            ],
                            'subdomains': {
                                'expense': {
                                    'security_groups': [
                                        'accounting-transactions-expense-sensitive'
                                    ]
                                },
                            },
                        },
                    }
                },
                'finance_management': {
                    'subdomains': {
                        'finance_master': {'security_groups': ['finance-master']}
                    }
                },
                'survey': {
                    'security_groups': [
                        'survey-lexus-anylt-us',
                        'survey-toyota-anylt-us',
                        'survey-lexus-anylt-puertorico',
                        'survey-toyota-anylt-puertorico',
                    ],
                    'subdomains': {'quality': {'security_groups': ['survey-quality']}},
                },
                'irm_business_confidential_domains': {
                    'subdomains': {
                        'cmbs_cmbk': {
                            'security_groups': [
                                'irm-profit-sen',
                                'irm-pl-fio-sen',
                                'irm-pl-ppo-sen',
                                'irm-pl-veh-entr-sen',
                                'irm-pl-veh-sal-sen',
                            ]
                        },
                        'pricing_cals': {
                            'subdomains': {
                                'cal_tema': {'security_groups': ['irm-pricing-tema-cal']},
                                'cal_tmc': {'security_groups': ['irm-pricing-tmc-cal']},
                                'cal_tms': {'security_groups': ['irm-pricing-tms-cal']},
                                'hon_tema': {'security_groups': ['irm-pricing-tema-hon']},
                            }
                        },
                        'pricing_4levels': {'security_groups': ['irm-pricing-4levels']},
                    }
                },
                'legal': {'security_groups': ['legal-busers']},
            }
        },
        'horizontal_business_functions': {
            'domains': {
                'reference': {
                    'security_groups': ['reference', 'reference-sensitive'],
                    'subdomains': {
                        'calendar': {'security_groups': ['reference-calendar']}
                    },
                    'facilities': {'security_groups': ['facility']},
                    'identity_management': {
                        'security_groups': ['identity-management'],
                        'subdomains': {
                            'pdc': {
                                'subdomains': {
                                    'labor': {'security_groups': ['parts-pdc-labor']}
                                }
                            }
                        },
                    },
                    'service_desk': {'security_groups': ['service-desk']},
                }
            },
        },
    }
}
