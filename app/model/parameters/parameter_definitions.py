"""
Defines the structure and values for all blood test parameters.
This module serves as the single source of truth for parameter definitions.
"""

RBC_PARAMETER = {
    'id': 'RBC',
    'name': 'Red Blood Cell Count',
    'group': 'CBC',
    'display_order': 1,

    'unit': {
        'standard': 'million cells/mcL',
        'alternative': ['million cells/mm³'],
        'conversion_factors': {
            'million cells/mm³': 1
        }
    },

    'ranges': {
        'standard': {
            'min': 4.5,
            'max': 5.5,
            'critical_low': 2.5,
            'critical_high': 7.0
        },
        'gender_specific': {
            'male': {
                'min': 4.7,
                'max': 6.1,
                'critical_low': 2.5,
                'critical_high': 7.0
            },
            'female': {
                'min': 4.2,
                'max': 5.4,
                'critical_low': 2.5,
                'critical_high': 7.0
            }
        },
        'age_specific': {
            'newborn': {'min': 4.8, 'max': 7.1},
            'child': {'min': 4.0, 'max': 5.5},
            'adult': {'min': 4.5, 'max': 5.5},
            'elderly': {'min': 4.0, 'max': 5.6}
        }
    },

    'classifications': {
        'very_low': {'min': 0, 'max': 3.5},
        'low': {'min': 3.5, 'max': 4.5},
        'normal': {'min': 4.5, 'max': 5.5},
        'high': {'min': 5.5, 'max': 6.5},
        'very_high': {'min': 6.5, 'max': float('inf')}
    },

    'validation': {
        'rules': ['one_decimal_place', 'positive_only'],
        'decimal_places': 1,
        'thresholds': {
            'warning_percentage': 10,
            'critical_percentage': 20
        }
    },

    'clinical_info': {
        'description': 'Red Blood Cells that carry oxygen throughout the body',
        'function': 'Transport oxygen from lungs to tissues and carbon dioxide from tissues to lungs',
        'common_conditions': {
            'high': [
                'Polycythemia',
                'Dehydration',
                'Lung disease',
                'High altitude adaptation'
            ],
            'low': [
                'Anemia',
                'Blood loss',
                'Bone marrow problems',
                'Chronic kidney disease',
                'Nutritional deficiencies'
            ]
        },
        'risk_factors': [
            'Smoking',
            'High altitude living',
            'Dehydration',
            'Chronic lung disease'
        ],
        'lifestyle_factors': [
            'Hydration status',
            'Physical activity level',
            'Altitude',
            'Smoking status'
        ],
        'medications': {
            'affecting': [
                'Erythropoiesis-stimulating agents',
                'Iron supplements',
                'Chemotherapy drugs'
            ],
            'affected_by': ['Hemoglobin', 'Hematocrit']
        }
    },

    'test_requirements': {
        'fasting_required': False,
        'fasting_duration': 0,
        'time_of_day': 'any',
        'special_requirements': ['Standard venipuncture'],
        'interfering_factors': [
            'Recent exercise',
            'Dehydration',
            'Recent blood transfusion',
            'High altitude'
        ]
    },

    'result_handling': {
        'validity_period': '24 hours',
        'storage_conditions': 'Room temperature',
        'critical_value_protocol': 'Notify healthcare provider if outside critical ranges',
        'repeat_test_interval': '3 months'
    },

    'correlations': {
        'related_parameters': ['Hemoglobin', 'Hematocrit', 'MCV', 'MCH', 'MCHC'],
        'relationships': [
            {
                'parameter': 'Hemoglobin',
                'relationship_type': 'direct',
                'description': 'RBC count typically correlates directly with hemoglobin levels'
            },
            {
                'parameter': 'Hematocrit',
                'relationship_type': 'direct',
                'description': 'RBC count directly relates to hematocrit percentage'
            }
        ],
        'calculations': {
            'formula': 'None - Direct measurement',
            'required_parameters': []
        }
    },

    'display': {
        'color_coding': True,
        'chart_type': 'line',
        'trend_analysis': True,
        'alert_levels': {
            'warning': 10,
            'critical': 20
        },
        'decimal_display': 1
    }
}

WBC_PARAMETER = {
    'id': 'WBC',
    'name': 'White Blood Cell Count',
    'group': 'CBC',
    'display_order': 2,

    'unit': {
        'standard': 'cells/mcL',
        'alternative': ['cells/mm³'],
        'conversion_factors': {
            'cells/mm³': 1
        }
    },

    'ranges': {
        'standard': {
            'min': 4500,
            'max': 11000,
            'critical_low': 2000,
            'critical_high': 50000
        },
        'gender_specific': {
            'male': {
                'min': 4500,
                'max': 11000,
                'critical_low': 2000,
                'critical_high': 50000
            },
            'female': {
                'min': 4500,
                'max': 11000,
                'critical_low': 2000,
                'critical_high': 50000
            }
        },
        'age_specific': {
            'newborn': {'min': 9000, 'max': 30000},
            'child': {'min': 5000, 'max': 14500},
            'adult': {'min': 4500, 'max': 11000},
            'elderly': {'min': 4000, 'max': 10500}
        }
    },

    'classifications': {
        'very_low': {'min': 0, 'max': 3000},
        'low': {'min': 3000, 'max': 4500},
        'normal': {'min': 4500, 'max': 11000},
        'high': {'min': 11000, 'max': 15000},
        'very_high': {'min': 15000, 'max': float('inf')}
    },

    'validation': {
        'rules': ['whole_numbers_only', 'positive_only'],
        'decimal_places': 0,
        'thresholds': {
            'warning_percentage': 10,
            'critical_percentage': 20
        }
    },

    'clinical_info': {
        'description': 'White Blood Cells that fight infection and disease',
        'function': 'Immune system defense against infections and diseases',
        'common_conditions': {
            'high': [
                'Infection',
                'Inflammation',
                'Leukemia',
                'Stress',
                'Allergic responses'
            ],
            'low': [
                'Bone marrow problems',
                'Viral infections',
                'Severe infections',
                'Autoimmune disorders',
                'Chemotherapy effects'
            ]
        },
        'risk_factors': [
            'Recent infection',
            'Autoimmune conditions',
            'Cancer',
            'Medications',
            'Chronic stress'
        ],
        'lifestyle_factors': [
            'Stress levels',
            'Sleep patterns',
            'Exercise intensity',
            'Smoking'
        ],
        'medications': {
            'affecting': [
                'Corticosteroids',
                'Chemotherapy drugs',
                'Some antibiotics',
                'Immunosuppressants'
            ],
            'affected_by': ['Neutrophils', 'Lymphocytes']
        }
    },

    'test_requirements': {
        'fasting_required': False,
        'fasting_duration': 0,
        'time_of_day': 'any',
        'special_requirements': ['Standard venipuncture'],
        'interfering_factors': [
            'Recent exercise',
            'Stress',
            'Medications (steroids)',
            'Time of day',
            'Recent infections'
        ]
    },

    'result_handling': {
        'validity_period': '24 hours',
        'storage_conditions': 'Room temperature',
        'critical_value_protocol': 'Immediate physician notification for critical values',
        'repeat_test_interval': 'As clinically indicated'
    },

    'correlations': {
        'related_parameters': [
            'Neutrophils',
            'Lymphocytes',
            'Monocytes',
            'Eosinophils',
            'Basophils'
        ],
        'relationships': [
            {
                'parameter': 'Neutrophils',
                'relationship_type': 'component',
                'description': 'Usually makes up 40-60% of total WBC'
            },
            {
                'parameter': 'Lymphocytes',
                'relationship_type': 'component',
                'description': 'Usually makes up 20-40% of total WBC'
            }
        ],
        'calculations': {
            'formula': 'Sum of all white blood cell types',
            'required_parameters': [
                'Neutrophils',
                'Lymphocytes',
                'Monocytes',
                'Eosinophils',
                'Basophils'
            ]
        }
    },

    'display': {
        'color_coding': True,
        'chart_type': 'line',
        'trend_analysis': True,
        'alert_levels': {
            'warning': 10,
            'critical': 20
        },
        'decimal_display': 0
    }
}

HEMOGLOBIN_PARAMETER = {
    'id': 'Hemoglobin',
    'name': 'Hemoglobin',
    'group': 'CBC',
    'display_order': 3,

    'unit': {
        'standard': 'g/dL',
        'alternative': ['g/L'],
        'conversion_factors': {
            'g/L': 10  # Multiply by 10 to convert g/dL to g/L
        }
    },

    'ranges': {
        'standard': {
            'min': 12.0,
            'max': 17.5,
            'critical_low': 7.0,
            'critical_high': 20.0
        },
        'gender_specific': {
            'male': {
                'min': 13.5,
                'max': 17.5,
                'critical_low': 7.0,
                'critical_high': 20.0
            },
            'female': {
                'min': 12.0,
                'max': 15.5,
                'critical_low': 7.0,
                'critical_high': 20.0,
                'condition_specific': {
                    'pregnancy': {
                        'first_trimester': {'min': 11.0, 'max': 14.0},
                        'second_trimester': {'min': 10.5, 'max': 14.0},
                        'third_trimester': {'min': 11.0, 'max': 14.0}
                    }
                }
            }
        },
        'age_specific': {
            'newborn': {'min': 14.0, 'max': 24.0},
            'infant_1_month': {'min': 10.0, 'max': 20.0},
            'child': {'min': 11.0, 'max': 16.0},
            'adult_male': {'min': 13.5, 'max': 17.5},
            'adult_female': {'min': 12.0, 'max': 15.5},
            'elderly': {'min': 12.0, 'max': 16.0}
        }
    },

    'classifications': {
        'very_low': {'min': 0, 'max': 9.0},
        'low': {'min': 9.0, 'max': 12.0},
        'normal': {'min': 12.0, 'max': 17.5},
        'high': {'min': 17.5, 'max': 20.0},
        'very_high': {'min': 20.0, 'max': float('inf')}
    },

    'validation': {
        'rules': ['one_decimal_place', 'gender_specific'],
        'decimal_places': 1,
        'thresholds': {
            'warning_percentage': 10,
            'critical_percentage': 20
        }
    },

    'clinical_info': {
        'description': 'Protein in red blood cells that carries oxygen',
        'function': 'Transports oxygen from lungs to tissues and assists in carbon dioxide removal',
        'common_conditions': {
            'general': {
                'high': [
                    'Polycythemia',
                    'Dehydration',
                    'Lung disease',
                    'Congenital heart disease',
                    'Living at high altitude'
                ],
                'low': [
                    'Anemia',
                    'Blood loss',
                    'Chronic kidney disease',
                    'Nutritional deficiencies',
                    'Bone marrow disorders'
                ]
            },
            'female': {
                'low': [
                    'Pregnancy'
                ]
            },
            'male': {
                'high': [],
                'low': []
            }
        },
        'risk_factors': {
            'general': [
                'Smoking',
                'High altitude living',
                'Chronic diseases',
                'Nutritional status'
            ],
            'female': [
                'Pregnancy'
            ],
            'male': []
        },
        'lifestyle_factors': {
            'general': [
                'Diet (Iron intake)',
                'Exercise',
                'Smoking',
                'Altitude',
                'Hydration status'
            ],
            'female': [],
            'male': []
        },
        'medications': {
            'affecting': [
                'Iron supplements',
                'Erythropoiesis-stimulating agents',
                'Chemotherapy drugs',
                'Some antibiotics'
            ],
            'affected_by': ['RBC', 'Iron']
        }
    },

    'test_requirements': {
        'fasting_required': False,
        'fasting_duration': 0,
        'time_of_day': 'any',
        'special_requirements': ['Standard venipuncture'],
        'interfering_factors': {
            'general': [
                'Recent exercise',
                'Altitude',
                'Smoking status',
                'Hydration status',
                'Recent blood transfusion'
            ],
            'female': [],
            'male': []
        }
    },

    'result_handling': {
        'validity_period': '24 hours',
        'storage_conditions': 'Room temperature',
        'critical_value_protocol': 'Urgent medical evaluation required for critical values',
        'repeat_test_interval': '3 months or as clinically indicated'
    },

    'correlations': {
        'related_parameters': ['RBC', 'Hematocrit', 'Iron', 'Ferritin'],
        'relationships': [
            {
                'parameter': 'Hematocrit',
                'relationship_type': 'direct',
                'description': 'Hematocrit should be approximately 3 times the hemoglobin value'
            },
            {
                'parameter': 'RBC',
                'relationship_type': 'direct',
                'description': 'Should correlate directly with RBC count'
            }
        ],
        'calculations': {
            'formula': 'MCHC = (Hemoglobin / Hematocrit) × 100',
            'required_parameters': ['Hematocrit']
        }
    },

    'display': {
        'color_coding': True,
        'chart_type': 'line',
        'trend_analysis': True,
        'alert_levels': {
            'warning': 10,
            'critical': 20
        },
        'decimal_display': 1
    }
}

HEMATOCRIT_PARAMETER = {
    'id': 'Hematocrit',
    'name': 'Hematocrit',
    'group': 'CBC',
    'display_order': 4,

    'unit': {
        'standard': '%',
        'alternative': ['L/L'],
        'conversion_factors': {
            'L/L': 0.01  # Multiply by 0.01 to convert from % to L/L
        }
    },

    'ranges': {
        'standard': {
            'min': 36,
            'max': 50,
            'critical_low': 21,
            'critical_high': 60
        },
        'gender_specific': {
            'male': {
                'min': 41,
                'max': 50,
                'critical_low': 21,
                'critical_high': 60
            },
            'female': {
                'min': 36,
                'max': 48,
                'critical_low': 21,
                'critical_high': 60,
                'condition_specific': {
                    'pregnancy': {
                        'first_trimester': {'min': 33, 'max': 42},
                        'second_trimester': {'min': 32, 'max': 42},
                        'third_trimester': {'min': 33, 'max': 42}
                    }
                }
            }
        },
        'age_specific': {
            'newborn': {'min': 42, 'max': 65},
            'infant_1_month': {'min': 31, 'max': 55},
            'child': {'min': 33, 'max': 49},
            'adult_male': {'min': 41, 'max': 50},
            'adult_female': {'min': 36, 'max': 48},
            'elderly': {'min': 35, 'max': 47}
        }
    },

    'classifications': {
        'very_low': {'min': 0, 'max': 30},
        'low': {'min': 30, 'max': 36},
        'normal': {'min': 36, 'max': 50},
        'high': {'min': 50, 'max': 55},
        'very_high': {'min': 55, 'max': float('inf')}
    },

    'validation': {
        'rules': ['gender_specific', 'whole_numbers_only'],
        'decimal_places': 0,
        'thresholds': {
            'warning_percentage': 10,
            'critical_percentage': 20
        }
    },

    'clinical_info': {
        'description': 'Percentage of blood volume that is red blood cells',
        'function': 'Indicates the proportion of blood composed of red blood cells',
        'common_conditions': {
            'general': {
                'high': [
                    'Dehydration',
                    'Polycythemia',
                    'COPD',
                    'Congenital heart disease',
                    'High altitude adaptation'
                ],
                'low': [
                    'Anemia',
                    'Blood loss',
                    'Hemodilution',
                    'Bone marrow failure',
                    'Nutritional deficiencies'
                ]
            },
            'female': {
                'low': [
                    'Pregnancy'
                ]
            },
            'male': {
                'high': [],
                'low': []
            }
        },
        'risk_factors': {
            'general': [
                'Dehydration',
                'High altitude',
                'Chronic lung disease',
                'Smoking'
            ],
            'female': [
                'Pregnancy'
            ],
            'male': []
        },
        'lifestyle_factors': {
            'general': [
                'Hydration status',
                'Physical activity',
                'Altitude',
                'Smoking status'
            ],
            'female': [],
            'male': []
        },
        'medications': {
            'affecting': [
                'Diuretics',
                'Blood thinners',
                'Erythropoiesis-stimulating agents',
                'Chemotherapy drugs'
            ],
            'affected_by': ['Hemoglobin', 'RBC']
        }
    },

    'test_requirements': {
        'fasting_required': False,
        'fasting_duration': 0,
        'time_of_day': 'any',
        'special_requirements': ['Standard venipuncture'],
        'interfering_factors': {
            'general': [
                'Hydration status',
                'Altitude',
                'Recent transfusion',
                'Body position during collection'
            ],
            'female': [
                'Pregnancy'
            ],
            'male': []
        }
    },

    'result_handling': {
        'validity_period': '24 hours',
        'storage_conditions': 'Room temperature',
        'critical_value_protocol': 'Urgent medical evaluation required for critical values',
        'repeat_test_interval': '3 months or as clinically indicated'
    },

    'correlations': {
        'related_parameters': ['Hemoglobin', 'RBC'],
        'relationships': [
            {
                'parameter': 'Hemoglobin',
                'relationship_type': 'direct',
                'description': 'Hematocrit is approximately 3 times the hemoglobin value'
            },
            {
                'parameter': 'RBC',
                'relationship_type': 'direct',
                'description': 'Directly correlates with RBC count'
            }
        ],
        'calculations': {
            'formula': 'Hematocrit ≈ Hemoglobin × 3 (±3)',
            'required_parameters': ['Hemoglobin']
        }
    },

    'display': {
        'color_coding': True,
        'chart_type': 'line',
        'trend_analysis': True,
        'alert_levels': {
            'warning': 10,
            'critical': 20
        },
        'decimal_display': 0
    }
}

PLATELETS_PARAMETER = {
    'id': 'Platelets',
    'name': 'Platelets',
    'group': 'CBC',
    'display_order': 5,

    'unit': {
        'standard': '/mcL',
        'alternative': ['/mm³'],
        'conversion_factors': {
            '/mm³': 1
        }
    },

    'ranges': {
        'standard': {
            'min': 150000,
            'max': 450000,
            'critical_low': 20000,
            'critical_high': 1000000
        },
        'gender_specific': {
            'male': {
                'min': 150000,
                'max': 450000,
                'critical_low': 20000,
                'critical_high': 1000000
            },
            'female': {
                'min': 150000,
                'max': 450000,
                'critical_low': 20000,
                'critical_high': 1000000,
                'condition_specific': {
                    'pregnancy': {
                        'first_trimester': {'min': 150000, 'max': 400000},
                        'second_trimester': {'min': 150000, 'max': 400000},
                        'third_trimester': {'min': 100000, 'max': 400000}
                    }
                }
            }
        },
        'age_specific': {
            'newborn': {'min': 150000, 'max': 400000},
            'child': {'min': 150000, 'max': 450000},
            'adult': {'min': 150000, 'max': 450000},
            'elderly': {'min': 150000, 'max': 400000}
        }
    },

    'classifications': {
        'very_low': {'min': 0, 'max': 50000},
        'low': {'min': 50000, 'max': 150000},
        'normal': {'min': 150000, 'max': 450000},
        'high': {'min': 450000, 'max': 750000},
        'very_high': {'min': 750000, 'max': float('inf')}
    },

    'validation': {
        'rules': ['whole_numbers_only'],
        'decimal_places': 0,
        'thresholds': {
            'warning_percentage': 10,
            'critical_percentage': 20
        }
    },

    'clinical_info': {
        'description': 'Blood cells that help with blood clotting',
        'function': 'Essential for blood clotting and prevention of bleeding',
        'common_conditions': {
            'general': {
                'high': [
                    'Inflammation',
                    'Cancer',
                    'Iron deficiency',
                    'Post-splenectomy',
                    'Essential thrombocythemia'
                ],
                'low': [
                    'Viral infections',
                    'Some medications',
                    'Leukemia',
                    'ITP',
                    'Aplastic anemia',
                    'Chemotherapy'
                ]
            },
            'female': {
                'high': [],
                'low': []
            },
            'male': {
                'high': [],
                'low': []
            }
        },
        'risk_factors': {
            'general': [
                'Autoimmune conditions',
                'Certain medications',
                'Bone marrow disorders',
                'Spleen problems',
                'Chronic infections'
            ],
            'female': [],
            'male': []
        },
        'lifestyle_factors': {
            'general': [
                'Exercise',
                'Alcohol consumption',
                'Smoking',
                'Diet',
                'Stress levels'
            ],
            'female': [],
            'male': []
        },
        'medications': {
            'affecting': [
                'Heparin',
                'Chemotherapy drugs',
                'NSAIDs',
                'Some antibiotics'
            ],
            'affected_by': ['MPV']
        }
    },

    'test_requirements': {
        'fasting_required': False,
        'fasting_duration': 0,
        'time_of_day': 'any',
        'special_requirements': [
            'EDTA tube (purple top)',
            'Gentle mixing',
            'No shaking'
        ],
        'interfering_factors': {
            'general': [
                'Recent exercise',
                'Medications (heparin, chemotherapy)',
                'Sample clotting',
                'Collection technique',
                'Time of day'
            ],
            'female': [
                'Pregnancy'
            ],
            'male': []
        }
    },

    'result_handling': {
        'validity_period': '24 hours',
        'storage_conditions': 'Room temperature',
        'critical_value_protocol': 'Immediate hematology consult required for critical values',
        'repeat_test_interval': 'As clinically indicated'
    },

    'correlations': {
        'related_parameters': ['WBC', 'MPV'],
        'relationships': [
            {
                'parameter': 'MPV',
                'relationship_type': 'inverse',
                'description': 'Usually inversely related - younger platelets are larger'
            }
        ],
        'calculations': {
            'formula': 'Direct measurement',
            'required_parameters': []
        }
    },

    'display': {
        'color_coding': True,
        'chart_type': 'line',
        'trend_analysis': True,
        'alert_levels': {
            'warning': 10,
            'critical': 20
        },
        'decimal_display': 0
    }
}

GLUCOSE_PARAMETER = {
    'id': 'Glucose',
    'name': 'Glucose',
    'group': 'Basic Metabolic',
    'display_order': 1,

    'unit': {
        'standard': 'mg/dL',
        'alternative': ['mmol/L'],
        'conversion_factors': {
            'mmol/L': 0.0555  # Multiply by 0.0555 to convert mg/dL to mmol/L
        }
    },

    'ranges': {
        'standard': {
            'min': 70,
            'max': 100,
            'critical_low': 40,
            'critical_high': 500
        },
        'gender_specific': {
            'male': {
                'min': 70,
                'max': 100,
                'critical_low': 40,
                'critical_high': 500
            },
            'female': {
                'min': 70,
                'max': 100,
                'critical_low': 40,
                'critical_high': 500
            }
        },
        'age_specific': {
            'newborn': {'min': 40, 'max': 90},
            'child': {'min': 60, 'max': 100},
            'adult': {'min': 70, 'max': 100},
            'elderly': {'min': 70, 'max': 100}
        },
        'clinical_ranges': {
            'normal': {'min': 70, 'max': 100},
            'prediabetic': {'min': 100, 'max': 125},
            'diabetic': {'min': 126, 'max': None}
        }
    },

    'classifications': {
        'very_low': {'min': 0, 'max': 50},
        'low': {'min': 50, 'max': 70},
        'normal': {'min': 70, 'max': 100},
        'high': {'min': 100, 'max': 200},
        'very_high': {'min': 200, 'max': float('inf')}
    },

    'validation': {
        'rules': ['fasting_required', 'whole_numbers_only'],
        'decimal_places': 0,
        'thresholds': {
            'warning_percentage': 10,
            'critical_percentage': 20
        }
    },

    'clinical_info': {
        'description': 'Blood sugar level after fasting',
        'function': 'Primary energy source for cells; indicator of diabetes and other metabolic conditions',
        'common_conditions': {
            'high': [
                'Diabetes',
                'Prediabetes',
                'Stress',
                'Medications',
                'Cushing syndrome'
            ],
            'low': [
                'Hypoglycemia',
                'Liver problems',
                'Medications',
                'Insulin overuse',
                'Endocrine disorders'
            ]
        },
        'risk_factors': [
            'Family history of diabetes',
            'Obesity',
            'Sedentary lifestyle',
            'Age over 45',
            'Gestational diabetes history'
        ],
        'lifestyle_factors': [
            'Diet',
            'Exercise',
            'Weight',
            'Stress',
            'Sleep patterns'
        ],
        'medications': {
            'affecting': [
                'Insulin',
                'Oral diabetes medications',
                'Corticosteroids',
                'Beta blockers',
                'Antipsychotics'
            ],
            'affected_by': ['HbA1c']
        }
    },

    'test_requirements': {
        'fasting_required': True,
        'fasting_duration': 8,
        'time_of_day': 'morning',
        'special_requirements': [
            'No food or drink except water for 8 hours',
            'No smoking',
            'No exercise'
        ],
        'interfering_factors': [
            'Recent meals',
            'Stress',
            'Medications',
            'Exercise',
            'Time of day',
            'Illness'
        ]
    },

    'result_handling': {
        'validity_period': '24 hours',
        'storage_conditions': 'Refrigerated serum separation',
        'critical_value_protocol': 'Immediate medical attention for critical values',
        'repeat_test_interval': '3 months for diabetic monitoring'
    },

    'correlations': {
        'related_parameters': ['HbA1c', 'Insulin', 'C-peptide'],
        'relationships': [
            {
                'parameter': 'HbA1c',
                'relationship_type': 'direct',
                'description': 'HbA1c reflects average glucose over past 3 months'
            }
        ],
        'calculations': {
            'formula': 'Direct measurement',
            'required_parameters': []
        }
    },

    'display': {
        'color_coding': True,
        'chart_type': 'line',
        'trend_analysis': True,
        'alert_levels': {
            'warning': 10,
            'critical': 20
        },
        'decimal_display': 0
    }
}

# File: parameter_definitions_v3.py

CALCIUM_PARAMETER = {
    'id': 'Calcium',
    'name': 'Calcium',
    'group': 'Basic Metabolic',
    'display_order': 2,

    'unit': {
        'standard': 'mg/dL',
        'alternative': ['mmol/L'],
        'conversion_factors': {
            'mmol/L': 0.25  # Multiply by 0.25 to convert mg/dL to mmol/L
        }
    },

    'ranges': {
        'standard': {
            'min': 8.6,
            'max': 10.2,
            'critical_low': 7.0,
            'critical_high': 12.0
        },
        'gender_specific': {
            'male': {
                'min': 8.6,
                'max': 10.2,
                'critical_low': 7.0,
                'critical_high': 12.0
            },
            'female': {
                'min': 8.8,
                'max': 10.1,
                'critical_low': 7.0,
                'critical_high': 12.0
            }
        },
        'age_specific': {
            'newborn': {'min': 7.6, 'max': 10.4},
            'child': {'min': 8.8, 'max': 10.3},
            'adult': {'min': 8.6, 'max': 10.2},
            'elderly': {'min': 8.6, 'max': 10.2}
        },
        'condition_specific': {
            'pregnancy': {'min': 8.8, 'max': 10.4}
        }
    },

    'classifications': {
        'very_low': {'min': 0, 'max': 7.5},
        'low': {'min': 7.5, 'max': 8.6},
        'normal': {'min': 8.6, 'max': 10.2},
        'high': {'min': 10.2, 'max': 11.0},
        'very_high': {'min': 11.0, 'max': float('inf')}
    },

    'validation': {
        'rules': ['one_decimal_place'],
        'decimal_places': 1,
        'thresholds': {
            'warning_percentage': 10,
            'critical_percentage': 20
        }
    },

    'clinical_info': {
        'description': 'Mineral essential for bones, muscle function, and blood clotting',
        'function': 'Critical for nerve conduction, muscle contraction, bone health, and cellular signaling',
        'common_conditions': {
            'high': [
                'Hyperparathyroidism',
                'Cancer',
                'Kidney problems',
                'Excessive vitamin D',
                'Dehydration'
            ],
            'low': [
                'Vitamin D deficiency',
                'Hypoparathyroidism',
                'Malnutrition',
                'Kidney disease',
                'Magnesium deficiency'
            ]
        },
        'risk_factors': [
            'Parathyroid disorders',
            'Kidney disease',
            'Vitamin D deficiency',
            'Cancer',
            'Certain medications'
        ],
        'lifestyle_factors': [
            'Diet',
            'Vitamin D exposure',
            'Physical activity',
            'Smoking',
            'Alcohol consumption'
        ],
        'medications': {
            'affecting': [
                'Diuretics',
                'Lithium',
                'Bisphosphonates',
                'Corticosteroids',
                'Calcium supplements'
            ],
            'affected_by': ['Vitamin D', 'PTH', 'Albumin']
        }
    },

    'test_requirements': {
        'fasting_required': False,
        'fasting_duration': 0,
        'time_of_day': 'any',
        'special_requirements': ['Standard venipuncture'],
        'interfering_factors': [
            'Albumin levels',
            'pH changes',
            'Medications',
            'Recent IV fluids',
            'Tourniquet time'
        ]
    },

    'result_handling': {
        'validity_period': '24 hours',
        'storage_conditions': 'Room temperature',
        'critical_value_protocol': 'Urgent evaluation needed for critical values',
        'repeat_test_interval': 'As clinically indicated'
    },

    'correlations': {
        'related_parameters': ['Albumin', 'Vitamin D', 'PTH', 'Phosphorus'],
        'relationships': [
            {
                'parameter': 'Albumin',
                'relationship_type': 'direct',
                'description': 'Calcium levels should be corrected for albumin'
            },
            {
                'parameter': 'PTH',
                'relationship_type': 'inverse',
                'description': 'PTH increases as calcium decreases'
            }
        ],
        'calculations': {
            'formula': 'Corrected Calcium = Measured Calcium + 0.8 * (4.0 - Albumin)',
            'required_parameters': ['Albumin']
        }
    },

    'display': {
        'color_coding': True,
        'chart_type': 'line',
        'trend_analysis': True,
        'alert_levels': {
            'warning': 10,
            'critical': 20
        },
        'decimal_display': 1
    }
}

TOTAL_CHOLESTEROL_PARAMETER = {
    'id': 'TOTAL_CHOL',
    'name': 'Total Cholesterol',
    'group': 'Lipid Panel',
    'display_order': 1,

    'unit': {
        'standard': 'mg/dL',
        'alternative': ['mmol/L'],
        'conversion_factors': {
            'mmol/L': 0.0259  # Multiply mg/dL by this to get mmol/L
        }
    },

    'ranges': {
        'standard': {
            'min': 0,
            'max': 200,
            'critical_low': 100,  # Extremely low cholesterol can indicate underlying conditions
            'critical_high': 300  # Very high risk for cardiovascular events
        },
        'age_specific': {
            'child': {'min': 0, 'max': 170},
            'adolescent': {'min': 0, 'max': 190},
            'adult': {'min': 0, 'max': 200},
            'elderly': {'min': 0, 'max': 200}
        },
        'condition_specific': {
            'cardiovascular_disease': {'min': 0, 'max': 180},
            'diabetes': {'min': 0, 'max': 180},
            'familial_hypercholesterolemia': {'min': 0, 'max': 170}
        }
    },

    'classifications': {
        'optimal': {'min': 0, 'max': 200},
        'borderline_high': {'min': 200, 'max': 239},
        'high': {'min': 240, 'max': float('inf')}
    },

    'validation': {
        'rules': ['whole_numbers_only', 'positive_only'],
        'decimal_places': 0,
        'thresholds': {
            'warning_percentage': 10,
            'critical_percentage': 20
        }
    },

    'clinical_info': {
        'description': 'Total amount of all types of cholesterol in blood',
        'function': 'Essential for cell membrane formation, hormone production, and vitamin D synthesis',
        'common_conditions': {
            'high': [
                'Cardiovascular disease risk',
                'Atherosclerosis',
                'Familial hypercholesterolemia',
                'Hypothyroidism',
                'Poor diet',
                'Obesity'
            ],
            'low': [
                'Malnutrition',
                'Hyperthyroidism',
                'Liver disease',
                'Cancer',
                'Inflammation'
            ]
        },
        'risk_factors': [
            'Family history',
            'Poor diet',
            'Obesity',
            'Lack of exercise',
            'Smoking',
            'Age',
            'Diabetes'
        ],
        'lifestyle_factors': [
            'Diet high in saturated fats',
            'Physical inactivity',
            'Smoking status',
            'Alcohol consumption',
            'Stress levels'
        ],
        'medications': {
            'affecting': [
                'Statins',
                'Fibrates',
                'Niacin',
                'Ezetimibe',
                'Bile acid sequestrants'
            ],
            'affected_by': [
                'Corticosteroids',
                'Progestins',
                'Anabolic steroids'
            ]
        }
    },

    'test_requirements': {
        'fasting_required': True,
        'fasting_duration': 12,
        'time_of_day': 'morning',
        'special_requirements': [
            'Fast for 12 hours',
            'Water is allowed',
            'Avoid high-fat meals day before'
        ],
        'interfering_factors': [
            'Recent meals',
            'Pregnancy',
            'Acute illness',
            'Recent exercise',
            'Certain medications'
        ]
    },

    'result_handling': {
        'validity_period': '24 hours',
        'storage_conditions': 'Room temperature serum',
        'critical_value_protocol': 'Notify healthcare provider if >300 mg/dL',
        'repeat_test_interval': '6 months'
    },

    'correlations': {
        'related_parameters': ['HDL', 'LDL', 'Triglycerides'],
        'relationships': [
            {
                'parameter': 'LDL',
                'relationship_type': 'component',
                'description': 'Major component of total cholesterol'
            },
            {
                'parameter': 'HDL',
                'relationship_type': 'component',
                'description': 'Protective component of total cholesterol'
            }
        ],
        'calculations': {
            'formula': 'Total Cholesterol = HDL + LDL + (Triglycerides/5)',
            'required_parameters': ['HDL', 'LDL', 'Triglycerides']
        }
    },

    'display': {
        'color_coding': True,
        'chart_type': 'line',
        'trend_analysis': True,
        'alert_levels': {
            'warning': 10,
            'critical': 20
        },
        'decimal_display': 0
    }
}

HDL_PARAMETER = {
    'id': 'HDL',
    'name': 'HDL Cholesterol',
    'group': 'Lipid Panel',
    'display_order': 2,

    'unit': {
        'standard': 'mg/dL',
        'alternative': ['mmol/L'],
        'conversion_factors': {
            'mmol/L': 0.0259
        }
    },

    'ranges': {
        'standard': {
            'min': 40,
            'max': 90,
            'critical_low': 20,
            'critical_high': 100
        },
        'gender_specific': {
            'male': {
                'min': 40,
                'max': 90,
                'critical_low': 20,
                'critical_high': 100
            },
            'female': {
                'min': 50,  # Women naturally have higher HDL levels
                'max': 90,
                'critical_low': 30,
                'critical_high': 100
            }
        },
        'age_specific': {
            'child': {'min': 45, 'max': 90},
            'adolescent': {'min': 40, 'max': 90},
            'adult': {'min': 40, 'max': 90},
            'elderly': {'min': 40, 'max': 90}
        },
        'condition_specific': {
            'metabolic_syndrome': {'min': 50, 'max': 90},
            'diabetes': {'min': 50, 'max': 90},
            'cardiovascular_disease': {'min': 50, 'max': 90}
        }
    },

    'classifications': {
        'very_low': {'min': 0, 'max': 30},
        'low': {'min': 31, 'max': 40},
        'borderline': {'min': 41, 'max': 49},
        'optimal': {'min': 50, 'max': 90},
        'high': {'min': 91, 'max': float('inf')}
    },

    'validation': {
        'rules': ['whole_numbers_only', 'positive_only', 'gender_specific'],
        'decimal_places': 0,
        'thresholds': {
            'warning_percentage': 10,
            'critical_percentage': 20
        }
    },

    'clinical_info': {
        'description': '"Good" cholesterol that helps remove excess cholesterol from blood vessels',
        'function': 'Transports excess cholesterol from tissues to liver for processing',
        'common_conditions': {
            'general': {
                'low': [
                    'Cardiovascular disease risk',
                    'Metabolic syndrome',
                    'Type 2 diabetes',
                    'Obesity',
                    'Physical inactivity',
                    'Smoking',
                    'Inflammation'
                ],
                'high': [
                    'Generally beneficial',
                    'Genetic variants (some rare conditions)',
                    'Regular physical activity',
                    'Healthy diet',
                    'Moderate alcohol consumption'
                ]
            },
            'female': {
                'low': [],
                'high': []
            },
            'male': {
                'low': [],
                'high': []
            }
        },
        'risk_factors': {
            'general': [
                'Sedentary lifestyle',
                'Poor diet',
                'Smoking',
                'Obesity',
                'Genetic factors',
                'Certain medications'
            ],
            'female': [],
            'male': []
        },
        'lifestyle_factors': {
            'general': [
                'Regular exercise increases HDL',
                'Mediterranean diet beneficial',
                'Smoking decreases HDL',
                'Weight loss can increase HDL',
                'Moderate alcohol may increase HDL'
            ],
            'female': [],
            'male': []
        },
        'medications': {
            'affecting': [
                'Statins',
                'Fibrates',
                'Niacin',
                'Beta blockers',
                'Anabolic steroids (decrease HDL)',
                'Progestins'
            ],
            'affected_by': [
                'Anti-inflammatory medications',
                'Hormone replacement therapy'
            ]
        }
    },

    'test_requirements': {
        'fasting_required': True,
        'fasting_duration': 12,
        'time_of_day': 'morning',
        'special_requirements': [
            'Fast for 12 hours',
            'Water is allowed',
            'Avoid high-fat meals day before',
            'Avoid alcohol for 24 hours'
        ],
        'interfering_factors': {
            'general': [
                'Recent exercise',
                'Recent alcohol consumption',
                'Medications',
                'Acute illness',
                'Recent significant weight change'
            ],
            'female': [],
            'male': []
        }
    },

    'result_handling': {
        'validity_period': '24 hours',
        'storage_conditions': 'Room temperature serum',
        'critical_value_protocol': 'Notify healthcare provider if <20 mg/dL',
        'repeat_test_interval': '6 months'
    },

    'correlations': {
        'related_parameters': [
            'Total Cholesterol',
            'LDL',
            'Triglycerides',
            'Body Mass Index'
        ],
        'relationships': [
            {
                'parameter': 'Total Cholesterol',
                'relationship_type': 'component',
                'description': 'Component of total cholesterol calculation'
            },
            {
                'parameter': 'Triglycerides',
                'relationship_type': 'inverse',
                'description': 'Often inversely related'
            }
        ],
        'calculations': {
            'formula': 'HDL Ratio = Total Cholesterol/HDL',
            'required_parameters': ['Total Cholesterol']
        }
    },

    'display': {
        'color_coding': True,
        'chart_type': 'line',
        'trend_analysis': True,
        'alert_levels': {
            'warning': 10,
            'critical': 20
        },
        'decimal_display': 0
    }
}

LDL_PARAMETER = {
    'id': 'LDL',
    'name': 'LDL Cholesterol',
    'group': 'Lipid Panel',
    'display_order': 3,

    'unit': {
        'standard': 'mg/dL',
        'alternative': ['mmol/L'],
        'conversion_factors': {
            'mmol/L': 0.0259
        }
    },

    'ranges': {
        'standard': {
            'min': 0,
            'max': 100,
            'critical_low': 40,  # Very low levels may indicate underlying condition
            'critical_high': 190  # Very high cardiovascular risk
        },
        'age_specific': {
            'child': {'min': 0, 'max': 110},
            'adolescent': {'min': 0, 'max': 110},
            'adult': {'min': 0, 'max': 100},
            'elderly': {'min': 0, 'max': 100}
        },
        'condition_specific': {
            'cardiovascular_disease': {'min': 0, 'max': 70},
            'diabetes': {'min': 0, 'max': 70},
            'familial_hypercholesterolemia': {'min': 0, 'max': 100},
            'metabolic_syndrome': {'min': 0, 'max': 70}
        }
    },

    'classifications': {
        'optimal': {'min': 0, 'max': 100},
        'near_optimal': {'min': 100, 'max': 129},
        'borderline': {'min': 130, 'max': 159},
        'high': {'min': 160, 'max': 189},
        'very_high': {'min': 190, 'max': float('inf')}
    },

    'validation': {
        'rules': ['whole_numbers_only', 'positive_only'],
        'decimal_places': 0,
        'thresholds': {
            'warning_percentage': 10,
            'critical_percentage': 20
        }
    },

    'clinical_info': {
        'description': '"Bad" cholesterol that can build up in arteries and form plaques',
        'function': 'Transports cholesterol from liver to tissues',
        'common_conditions': {
            'high': [
                'Cardiovascular disease',
                'Atherosclerosis',
                'Familial hypercholesterolemia',
                'Hypothyroidism',
                'Diabetes',
                'Metabolic syndrome',
                'Poor diet',
                'Obesity'
            ],
            'low': [
                'Malnutrition',
                'Hyperthyroidism',
                'Severe illness',
                'Inflammation',
                'Some genetic conditions'
            ]
        },
        'risk_factors': [
            'Family history',
            'Poor diet',
            'Physical inactivity',
            'Obesity',
            'Smoking',
            'Age',
            'Diabetes',
            'High blood pressure'
        ],
        'lifestyle_factors': [
            'Diet high in saturated fats',
            'Lack of exercise',
            'Smoking',
            'Excessive alcohol',
            'Stress',
            'Poor sleep'
        ],
        'medications': {
            'affecting': [
                'Statins',
                'Ezetimibe',
                'PCSK9 inhibitors',
                'Bile acid sequestrants',
                'Niacin'
            ],
            'affected_by': [
                'Corticosteroids',
                'Progestins',
                'Beta blockers',
                'Diuretics'
            ]
        }
    },

    'test_requirements': {
        'fasting_required': True,
        'fasting_duration': 12,
        'time_of_day': 'morning',
        'special_requirements': [
            'Fast for 12 hours',
            'Water is allowed',
            'Avoid high-fat meals day before',
            'Avoid alcohol for 24 hours'
        ],
        'interfering_factors': [
            'Recent meals',
            'Acute illness',
            'Recent exercise',
            'Medications',
            'Pregnancy'
        ]
    },

    'result_handling': {
        'validity_period': '24 hours',
        'storage_conditions': 'Room temperature serum',
        'critical_value_protocol': 'Notify healthcare provider if >190 mg/dL',
        'repeat_test_interval': '6 months'
    },

    'correlations': {
        'related_parameters': [
            'Total Cholesterol',
            'HDL',
            'Triglycerides',
            'Non-HDL Cholesterol'
        ],
        'relationships': [
            {
                'parameter': 'Total Cholesterol',
                'relationship_type': 'component',
                'description': 'Major component of total cholesterol'
            },
            {
                'parameter': 'Triglycerides',
                'relationship_type': 'calculation',
                'description': 'Used in Friedewald formula for LDL calculation'
            }
        ],
        'calculations': {
            'formula': 'LDL = Total Cholesterol - HDL - (Triglycerides/5)',
            'required_parameters': ['Total Cholesterol', 'HDL', 'Triglycerides']
        }
    },

    'display': {
        'color_coding': True,
        'chart_type': 'line',
        'trend_analysis': True,
        'alert_levels': {
            'warning': 10,
            'critical': 20
        },
        'decimal_display': 0
    }
}

VITAMIN_D_PARAMETER = {
    'id': 'VIT_D',
    'name': 'Vitamin D',
    'group': 'Vitamins & Minerals',
    'display_order': 1,

    'unit': {
        'standard': 'ng/mL',
        'alternative': ['nmol/L'],
        'conversion_factors': {
            'nmol/L': 2.496  # Multiply ng/mL by this to get nmol/L
        }
    },

    'ranges': {
        'standard': {
            'min': 30,
            'max': 100,
            'critical_low': 10,
            'critical_high': 150
        },
        'gender_specific': {
            'male': {
                'min': 30,
                'max': 100,
                'critical_low': 10,
                'critical_high': 150
            },
            'female': {
                'min': 30,
                'max': 100,
                'critical_low': 10,
                'critical_high': 150,
                'condition_specific': {
                    'pregnancy': {'min': 40, 'max': 100}
                }
            }
        },
        'age_specific': {
            'infant': {'min': 20, 'max': 60},
            'child': {'min': 20, 'max': 60},
            'adult': {'min': 30, 'max': 100},
            'elderly': {'min': 30, 'max': 100}
        },
        'condition_specific': {
            'osteoporosis': {'min': 40, 'max': 100},
            'chronic_kidney_disease': {'min': 30, 'max': 100},
            'obesity': {'min': 40, 'max': 100}  # Higher targets due to reduced bioavailability
        }
    },

    'classifications': {
        'deficient': {'min': 0, 'max': 20},
        'insufficient': {'min': 21, 'max': 29},
        'sufficient': {'min': 30, 'max': 100},
        'high': {'min': 101, 'max': 150},
        'toxic': {'min': 151, 'max': float('inf')}
    },

    'validation': {
        'rules': ['one_decimal_place', 'positive_only'],
        'decimal_places': 1,
        'thresholds': {
            'warning_percentage': 15,
            'critical_percentage': 25
        }
    },

    'clinical_info': {
        'description': 'Fat-soluble vitamin essential for bone health, immune function, and cellular growth',
        'function': 'Calcium absorption, bone mineralization, immune regulation, cell differentiation',
        'common_conditions': {
            'general': {
                'low': [
                    'Osteoporosis',
                    'Rickets',
                    'Osteomalacia',
                    'Limited sun exposure',
                    'Dark skin',
                    'Obesity',
                    'Malabsorption disorders',
                    'Chronic kidney disease'
                ],
                'high': [
                    'Excessive supplementation',
                    'Granulomatous disorders',
                    'Primary hyperparathyroidism',
                    'Williams syndrome'
                ]
            },
            'female': {
                'low': [
                    'Pregnancy'
                ],
                'high': []
            },
            'male': {
                'low': [],
                'high': []
            }
        },
        'risk_factors': {
            'general': [
                'Limited sun exposure',
                'Northern latitudes',
                'Dark skin',
                'Obesity',
                'Poor diet',
                'Age > 65',
                'Malabsorption disorders'
            ],
            'female': [
                'Pregnancy'
            ],
            'male': []
        },
        'lifestyle_factors': {
            'general': [
                'Sunlight exposure',
                'Diet (fatty fish, fortified foods)',
                'Sunscreen use',
                'Indoor lifestyle',
                'Clothing coverage',
                'Geographic location'
            ],
            'female': [],
            'male': []
        },
        'medications': {
            'affecting': [
                'Anticonvulsants',
                'Glucocorticoids',
                'HIV medications',
                'Anti-fungals',
                'Cholestyramine'
            ],
            'affected_by': [
                'Calcium supplements',
                'Thyroid medications'
            ]
        }
    },

    'test_requirements': {
        'fasting_required': False,
        'fasting_duration': 0,
        'time_of_day': 'any',
        'special_requirements': [
            'No special timing required',
            'Recent sunlight exposure may affect levels'
        ],
        'interfering_factors': {
            'general': [
                'Season',
                'Latitude',
                'Time of day',
                'Skin pigmentation',
                'Sunscreen use',
                'Recent travel'
            ],
            'female': [],
            'male': []
        }
    },

    'result_handling': {
        'validity_period': '72 hours',
        'storage_conditions': 'Protected from light',
        'critical_value_protocol': 'Notify provider if <10 or >150 ng/mL',
        'repeat_test_interval': '3-6 months'
    },

    'correlations': {
        'related_parameters': [
            'Calcium',
            'Phosphorus',
            'PTH',
            'Alkaline Phosphatase'
        ],
        'relationships': [
            {
                'parameter': 'PTH',
                'relationship_type': 'inverse',
                'description': 'Low vitamin D typically increases PTH'
            },
            {
                'parameter': 'Calcium',
                'relationship_type': 'direct',
                'description': 'Vitamin D increases calcium absorption'
            }
        ],
        'calculations': {
            'formula': None,
            'required_parameters': []
        }
    },

    'display': {
        'color_coding': True,
        'chart_type': 'line',
        'trend_analysis': True,
        'alert_levels': {
            'warning': 15,
            'critical': 25
        },
        'decimal_display': 1
    }
}

VITAMIN_B12_PARAMETER = {
    'id': 'VIT_B12',
    'name': 'Vitamin B12',
    'group': 'Vitamins & Minerals',
    'display_order': 2,

    'unit': {
        'standard': 'pg/mL',
        'alternative': ['pmol/L'],
        'conversion_factors': {
            'pmol/L': 0.738  # Multiply pg/mL by this to get pmol/L
        }
    },

    'ranges': {
        'standard': {
            'min': 200,
            'max': 900,
            'critical_low': 100,
            'critical_high': 2000
        },
        'gender_specific': {
            'male': {
                'min': 200,
                'max': 900,
                'critical_low': 100,
                'critical_high': 2000
            },
            'female': {
                'min': 200,
                'max': 900,
                'critical_low': 100,
                'critical_high': 2000,
                'condition_specific': {
                    'pregnancy': {'min': 300, 'max': 900}
                }
            }
        },
        'age_specific': {
            'infant': {'min': 200, 'max': 900},
            'child': {'min': 200, 'max': 900},
            'adult': {'min': 200, 'max': 900},
            'elderly': {'min': 300, 'max': 900}  # Higher minimum due to decreased absorption
        },
        'condition_specific': {
            'vegan_diet': {'min': 300, 'max': 900},
            'pernicious_anemia': {'min': 300, 'max': 900},
            'gastric_surgery': {'min': 300, 'max': 900}
        }
    },

    'classifications': {
        'deficient': {'min': 0, 'max': 200},
        'borderline': {'min': 201, 'max': 300},
        'optimal': {'min': 301, 'max': 900},
        'high': {'min': 901, 'max': 2000},
        'very_high': {'min': 2001, 'max': float('inf')}
    },

    'validation': {
        'rules': ['whole_numbers_only', 'positive_only'],
        'decimal_places': 0,
        'thresholds': {
            'warning_percentage': 15,
            'critical_percentage': 25
        }
    },

    'clinical_info': {
        'description': 'Essential vitamin for nerve function, DNA synthesis, and red blood cell formation',
        'function': 'DNA synthesis, nerve myelination, red blood cell formation, homocysteine metabolism',
        'common_conditions': {
            'general': {
                'low': [
                    'Pernicious anemia',
                    'Veganism/vegetarianism',
                    'Gastric surgery',
                    'Celiac disease',
                    'Crohn\'s disease',
                    'Elderly age',
                    'H. pylori infection',
                    'Metformin use'
                ],
                'high': [
                    'B12 supplementation',
                    'Liver disease',
                    'Myeloproliferative disorders',
                    'Severe liver disease'
                ]
            },
            'female': {
                'low': [
                    'Pregnancy'
                ],
                'high': []
            },
            'male': {
                'low': [],
                'high': []
            }
        },
        'risk_factors': {
            'general': [
                'Vegan/vegetarian diet',
                'Age > 60',
                'Gastric surgery',
                'Autoimmune disorders',
                'Chronic alcoholism',
                'Metformin use',
                'Proton pump inhibitors'
            ],
            'female': [
                'Pregnancy'
            ],
            'male': []
        },
        'lifestyle_factors': {
            'general': [
                'Dietary intake of animal products',
                'Alcohol consumption',
                'Strict vegetarian/vegan diet',
                'Use of supplements'
            ],
            'female': [],
            'male': []
        },
        'medications': {
            'affecting': [
                'Metformin',
                'Proton pump inhibitors',
                'H2 blockers',
                'Nitrous oxide',
                'Colchicine'
            ],
            'affected_by': [
                'Oral contraceptives',
                'Antibiotics'
            ]
        }
    },

    'test_requirements': {
        'fasting_required': False,
        'fasting_duration': 0,
        'time_of_day': 'morning preferred',
        'special_requirements': [
            'Stop B12 supplements 48 hours before test',
            'Morning collection preferred'
        ],
        'interfering_factors': {
            'general': [
                'Recent B12 supplementation',
                'Recent meal high in animal protein',
                'Folate deficiency',
                'Multiple myeloma',
                'Liver disease'
            ],
            'female': [],
            'male': []
        }
    },

    'result_handling': {
        'validity_period': '72 hours',
        'storage_conditions': 'Refrigerated serum',
        'critical_value_protocol': 'Notify provider if <100 pg/mL',
        'repeat_test_interval': '3-12 months'
    },

    'correlations': {
        'related_parameters': [
            'Folate',
            'MCV',
            'Homocysteine',
            'Methylmalonic acid',
            'Complete Blood Count'
        ],
        'relationships': [
            {
                'parameter': 'MCV',
                'relationship_type': 'inverse',
                'description': 'Low B12 often associated with high MCV'
            },
            {
                'parameter': 'Homocysteine',
                'relationship_type': 'inverse',
                'description': 'Low B12 associated with elevated homocysteine'
            }
        ],
        'calculations': {
            'formula': None,
            'required_parameters': []
        }
    },

    'display': {
        'color_coding': True,
        'chart_type': 'line',
        'trend_analysis': True,
        'alert_levels': {
            'warning': 15,
            'critical': 25
        },
        'decimal_display': 0
    }
}
IRON_PARAMETER = {
    'id': 'IRON',
    'name': 'Iron',
    'group': 'Vitamins & Minerals',
    'display_order': 3,

    'unit': {
        'standard': 'μg/dL',
        'alternative': ['μmol/L'],
        'conversion_factors': {
            'μmol/L': 0.179  # Multiply μg/dL by this to get μmol/L
        }
    },

    'ranges': {
        'standard': {
            'min': 60,
            'max': 170,
            'critical_low': 30,
            'critical_high': 400
        },
        'gender_specific': {
            'male': {
                'min': 65,
                'max': 175,
                'critical_low': 30,
                'critical_high': 400
            },
            'female': {
                'min': 50,
                'max': 170,
                'critical_low': 30,
                'critical_high': 400,
                'condition_specific': {
                    'pregnancy': {
                        'first_trimester': {'min': 40, 'max': 170},
                        'second_trimester': {'min': 35, 'max': 145},
                        'third_trimester': {'min': 30, 'max': 140}
                    },
                    'menstruation': {'min': 50, 'max': 170}
                }
            }
        },
        'age_specific': {
            'infant': {'min': 40, 'max': 100},
            'child': {'min': 50, 'max': 120},
            'adolescent_male': {'min': 65, 'max': 175},
            'adolescent_female': {'min': 50, 'max': 170},
            'adult_male': {'min': 65, 'max': 175},
            'adult_female': {'min': 50, 'max': 170},
            'elderly': {'min': 50, 'max': 150}
        },
        'condition_specific': {
            'inflammatory_conditions': {'min': 40, 'max': 150}
        }
    },

    'classifications': {
        'severe_deficiency': {'min': 0, 'max': 30},
        'deficient': {'min': 31, 'max': 50},
        'borderline': {'min': 51, 'max': 60},
        'normal': {'min': 61, 'max': 170},
        'elevated': {'min': 171, 'max': 300},
        'toxic': {'min': 301, 'max': float('inf')}
    },

    'validation': {
        'rules': ['whole_numbers_only', 'positive_only', 'gender_specific'],
        'decimal_places': 0,
        'thresholds': {
            'warning_percentage': 15,
            'critical_percentage': 25
        }
    },

    'clinical_info': {
        'description': 'Essential mineral for oxygen transport and cellular energy production',
        'function': 'Hemoglobin synthesis, oxygen transport, cellular metabolism, enzyme function',
        'common_conditions': {
            'general': {
                'high': [
                    'Hemochromatosis',
                    'Multiple transfusions',
                    'Iron supplementation',
                    'Hemolysis',
                    'Acute liver injury',
                    'Lead poisoning'
                ],
                'low': [
                    'Iron deficiency anemia',
                    'Chronic blood loss',
                    'Malabsorption',
                    'Chronic inflammation',
                    'Celiac disease',
                    'H. pylori infection'
                ]
            },
            'female': {
                'low': [
                    'Heavy menstruation',
                    'Pregnancy'
                ]
            },
            'male': {
                'high': [],
                'low': []
            }
        },
        'risk_factors': {
            'general': [
                'Vegetarian/vegan diet',
                'Blood donation',
                'Gastrointestinal disorders',
                'Chronic disease',
                'Endurance athletes'
            ],
            'female': [
                'Menstruation',
                'Pregnancy'
            ],
            'male': []
        },
        'lifestyle_factors': {
            'general': [
                'Dietary iron intake',
                'Vitamin C consumption',
                'Tea/coffee consumption',
                'Physical activity level'
            ],
            'female': [
                'Menstrual status'
            ],
            'male': []
        },
        'medications': {
            'affecting': [
                'Iron supplements',
                'Antacids',
                'Proton pump inhibitors',
                'Tetracyclines',
                'Calcium supplements'
            ],
            'affected_by': [
                'Oral contraceptives',
                'NSAIDs'
            ]
        }
    },

    'test_requirements': {
        'fasting_required': True,
        'fasting_duration': 12,
        'time_of_day': 'morning',
        'special_requirements': [
            'Morning collection preferred',
            'Fasting for 12 hours',
            'Stop iron supplements 24 hours before'
        ],
        'interfering_factors': {
            'general': [
                'Recent meals',
                'Time of day',
                'Recent iron supplementation',
                'Inflammation',
                'Infection',
                'Recent transfusion'
            ],
            'female': [
                'Pregnancy'
            ],
            'male': []
        }
    },

    'result_handling': {
        'validity_period': '24 hours',
        'storage_conditions': 'Refrigerated serum',
        'critical_value_protocol': 'Notify provider if <30 or >400 μg/dL',
        'repeat_test_interval': '2-3 months'
    },

    'correlations': {
        'related_parameters': [
            'Ferritin',
            'TIBC',
            'Transferrin',
            'Hemoglobin',
            'Hematocrit',
            'RBC'
        ],
        'relationships': [
            {
                'parameter': 'TIBC',
                'relationship_type': 'inverse',
                'description': 'Increases when iron is low'
            },
            {
                'parameter': 'Ferritin',
                'relationship_type': 'direct',
                'description': 'Usually correlates with iron stores'
            }
        ],
        'calculations': {
            'formula': 'Transferrin Saturation = (Serum Iron / TIBC) × 100',
            'required_parameters': ['TIBC']
        }
    },

    'display': {
        'color_coding': True,
        'chart_type': 'line',
        'trend_analysis': True,
        'alert_levels': {
            'warning': 15,
            'critical': 25
        },
        'decimal_display': 0
    }
}

BLOOD_PARAMETERS = {
    'CBC': {
        'parameter_metadata': {
            'description': 'Complete Blood Count - Basic blood test that measures different components of blood',
            'category_importance': 'critical',
            'display_order': 1
        },
        'parameters': {
            'RBC': RBC_PARAMETER,
            'WBC': WBC_PARAMETER,
            'Hemoglobin': HEMOGLOBIN_PARAMETER,
            'Hematocrit': HEMATOCRIT_PARAMETER,
            'Platelets': PLATELETS_PARAMETER
        }
    },

    'Basic Metabolic': {
        'parameter_metadata': {
            'description': 'Basic Metabolic Panel - Measures key metabolic functions',
            'category_importance': 'critical',
            'display_order': 2
        },
        'parameters': {
            'Glucose': GLUCOSE_PARAMETER,
            'Calcium': CALCIUM_PARAMETER
        }
    },

    'Lipid Panel': {
        'parameter_metadata': {
            'description': 'Measures various types of cholesterol and triglycerides',
            'category_importance': 'critical',
            'display_order': 3
        },
        'parameters': {
            'Total Cholesterol': TOTAL_CHOLESTEROL_PARAMETER,
            'HDL': HDL_PARAMETER,
            'LDL': LDL_PARAMETER
        }
    },

    'Vitamins & Minerals': {
        'parameter_metadata': {
            'description': 'Essential vitamins and minerals that play crucial roles in body functions',
            'category_importance': 'important',
            'display_order': 4
        },
        'parameters': {
            'Vitamin D': VITAMIN_D_PARAMETER,
            'Vitamin B12': VITAMIN_B12_PARAMETER,
            'Iron': IRON_PARAMETER
        }
    }
}

"""
Future Parameters to be Added:

1. Additional CBC Parameters:
    - Mean Corpuscular Volume (MCV)
     * Normal Range: 80-100 fL
     * Description: Average size of red blood cells

    - Mean Corpuscular Hemoglobin (MCH)
     * Normal Range: 27-31 pg
     * Description: Average amount of hemoglobin in red blood cells

    - Red Cell Distribution Width (RDW)
     * Normal Range: 11.5-14.5%
     * Description: Variation in red blood cell size

2. Extended Metabolic Panel:
    - Sodium
      * Normal Range: 135-145 mEq/L
    - Potassium
      * Normal Range: 3.5-5.0 mEq/L
    - Chloride
      * Normal Range: 96-106 mEq/L
    - CO2
      * Normal Range: 23-29 mEq/L
    - Creatinine
      * Normal Range: 0.7-1.3 mg/dL
    - BUN (Blood Urea Nitrogen)
      * Normal Range: 7-20 mg/dL

3. Extended Lipid Panel:
    - Triglycerides
      * Normal Range: < 150 mg/dL
    - VLDL Cholesterol
      * Normal Range: 2-30 mg/dL

4. Additional Vitamins/Minerals:
    - Folate
      * Normal Range: 2-20 ng/mL
    - Magnesium
      * Normal Range: 1.7-2.2 mg/dL
    - Zinc
      * Normal Range: 60-120 mcg/dL

Note: These parameters will be implemented following the same structure as existing parameters,
including gender-specific ranges where applicable, unit conversions, validation rules, and metadata.
"""