PRODUCT_MAPPING = {
        "settings": {
        "index": {
            "mapping": {
                "total_fields": {
                    "limit": 5000
                }
            },
            "number_of_shards": 3,
            "number_of_replicas": 1,
            "refresh_interval": "30s"
        },
        "analysis": {
            "filter": {
                "french_elision": {
                    "type": "elision",
                    "articles_case": True,
                    "articles": [
                        "l", "m", "t", "qu", "n", "s",
                        "j", "d", "c", "jusqu", "quoiqu",
                        "lorsqu", "puisqu"
                    ]
                },
                "french_stemmer": {
                    "type": "stemmer",
                    "language": "light_french"
                },
                "french_stop": {
                    "type": "stop",
                    "stopwords": "_french_"
                }
            },
            "analyzer": {
                "folding_analyzer": {
                    "tokenizer": "standard",
                    "filter": ["lowercase", "asciifolding"]
                },
                "search_french": {
                    "tokenizer": "standard",
                    "filter": [
                        "french_elision",
                        "lowercase",
                        "french_stop",
                        "french_stemmer",
                        "asciifolding"
                    ]
                }
            }
        }
    },
    "mappings": {
      "dynamic_templates": [
        {
          "ext_reference": {
            "path_match": "extensions.*.reference",
            "mapping": {
              "fields": {
                "text": {
                  "analyzer": "folding_analyzer",
                  "type": "search_as_you_type"
                }
              },
              "type": "keyword"
            }
          }
        },
        {
          "ext_name": {
            "path_match": "extensions.*.name",
            "mapping": {
              "fields": {
                "text": {
                  "analyzer": "folding_analyzer",
                  "type": "search_as_you_type"
                }
              },
              "type": "keyword"
            }
          }
        },
        {
          "ext_url": {
            "path_match": "extensions.*.url",
            "mapping": {
              "type": "keyword"
            }
          }
        },
        {
          "ext_score": {
            "path_match": "extensions.*.score",
            "mapping": {
              "type": "integer"
            }
          }
        },
        {
          "ext_price": {
            "path_match": "extensions.*.price",
            "mapping": {
              "type": "float"
            }
          }
        },
        {
          "ext_price_taxed": {
            "path_match": "extensions.*.price_taxed",
            "mapping": {
              "type": "float"
            }
          }
        },
        {
          "ext_discount_price": {
            "path_match": "extensions.*.discount_price",
            "mapping": {
              "type": "float"
            }
          }
        },
        {
          "ext_discount_price_taxed": {
            "path_match": "extensions.*.discount_price_taxed",
            "mapping": {
              "type": "float"
            }
          }
        },
        {
          "ext_average_rating": {
            "path_match": "extensions.*.average_rating",
            "mapping": {
              "type": "float"
            }
          }
        },
        {
          "ext_search_title": {
            "path_match": "extensions.*.search_title",
            "mapping": {
              "analyzer": "search_french",
              "type": "text"
            }
          }
        }
      ],
      "properties": {
        "accessories": {
          "type": "long"
        },
        "aliases": {
          "type": "nested",
          "properties": {
            "alias": {
              "type": "keyword",
              "fields": {
                "text": {
                  "type": "search_as_you_type",
                  "doc_values": "false",
                  "max_shingle_size": 3,
                  "analyzer": "folding_analyzer"
                }
              }
            },
            "category": {
              "type": "keyword"
            }
          }
        },
        "alternatives": {
          "type": "long"
        },
        "barcode": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "best_brand": {
          "properties": {
            "id": {
              "type": "long"
            },
            "label": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "name": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            }
          }
        },
        "best_image": {
          "properties": {
            "file": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "folder": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "size": {
              "type": "long"
            },
            "type": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "url": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            }
          }
        },
        "brand": {
          "properties": {
            "aliases": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "id": {
              "type": "long"
            },
            "image": {
              "properties": {
                "url": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "label": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "name": {
              "type": "search_as_you_type",
              "doc_values": "false",
              "max_shingle_size": 3,
              "analyzer": "folding_analyzer"
            }
          }
        },
        "categories": {
          "type": "nested",
          "properties": {
            "id": {
              "type": "long"
            },
            "label": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "name": {
              "type": "search_as_you_type",
              "doc_values": "false",
              "max_shingle_size": 3,
              "analyzer": "folding_analyzer"
            },
            "parent": {
              "properties": {
                "id": {
                  "type": "long"
                },
                "label": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "parent": {
                  "properties": {
                    "id": {
                      "type": "long"
                    },
                    "label": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "parent": {
                      "properties": {
                        "id": {
                          "type": "long"
                        },
                        "label": {
                          "type": "text",
                          "fields": {
                            "keyword": {
                              "type": "keyword",
                              "ignore_above": 256
                            }
                          }
                        },
                        "name": {
                          "type": "text",
                          "fields": {
                            "keyword": {
                              "type": "keyword",
                              "ignore_above": 256
                            }
                          }
                        },
                        "parent": {
                          "properties": {
                            "id": {
                              "type": "long"
                            },
                            "label": {
                              "type": "text",
                              "fields": {
                                "keyword": {
                                  "type": "keyword",
                                  "ignore_above": 256
                                }
                              }
                            },
                            "name": {
                              "type": "text",
                              "fields": {
                                "keyword": {
                                  "type": "keyword",
                                  "ignore_above": 256
                                }
                              }
                            },
                            "parent": {
                              "properties": {
                                "id": {
                                  "type": "long"
                                },
                                "label": {
                                  "type": "text",
                                  "fields": {
                                    "keyword": {
                                      "type": "keyword",
                                      "ignore_above": 256
                                    }
                                  }
                                },
                                "name": {
                                  "type": "text",
                                  "fields": {
                                    "keyword": {
                                      "type": "keyword",
                                      "ignore_above": 256
                                    }
                                  }
                                },
                                "parent": {
                                  "properties": {
                                    "id": {
                                      "type": "long"
                                    },
                                    "label": {
                                      "type": "text",
                                      "fields": {
                                        "keyword": {
                                          "type": "keyword",
                                          "ignore_above": 256
                                        }
                                      }
                                    },
                                    "name": {
                                      "type": "text",
                                      "fields": {
                                        "keyword": {
                                          "type": "keyword",
                                          "ignore_above": 256
                                        }
                                      }
                                    },
                                    "parent": {
                                      "properties": {
                                        "id": {
                                          "type": "long"
                                        },
                                        "label": {
                                          "type": "text",
                                          "fields": {
                                            "keyword": {
                                              "type": "keyword",
                                              "ignore_above": 256
                                            }
                                          }
                                        },
                                        "name": {
                                          "type": "text",
                                          "fields": {
                                            "keyword": {
                                              "type": "keyword",
                                              "ignore_above": 256
                                            }
                                          }
                                        },
                                        "picture": {
                                          "properties": {
                                            "url": {
                                              "type": "text",
                                              "fields": {
                                                "keyword": {
                                                  "type": "keyword",
                                                  "ignore_above": 256
                                                }
                                              }
                                            }
                                          }
                                        }
                                      }
                                    },
                                    "picture": {
                                      "properties": {
                                        "url": {
                                          "type": "text",
                                          "fields": {
                                            "keyword": {
                                              "type": "keyword",
                                              "ignore_above": 256
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
                                },
                                "picture": {
                                  "properties": {
                                    "url": {
                                      "type": "text",
                                      "fields": {
                                        "keyword": {
                                          "type": "keyword",
                                          "ignore_above": 256
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            },
                            "picture": {
                              "properties": {
                                "url": {
                                  "type": "text",
                                  "fields": {
                                    "keyword": {
                                      "type": "keyword",
                                      "ignore_above": 256
                                    }
                                  }
                                }
                              }
                            }
                          }
                        },
                        "picture": {
                          "properties": {
                            "url": {
                              "type": "text",
                              "fields": {
                                "keyword": {
                                  "type": "keyword",
                                  "ignore_above": 256
                                }
                              }
                            }
                          }
                        }
                      }
                    },
                    "picture": {
                      "properties": {
                        "url": {
                          "type": "text",
                          "fields": {
                            "keyword": {
                              "type": "keyword",
                              "ignore_above": 256
                            }
                          }
                        }
                      }
                    }
                  }
                },
                "picture": {
                  "properties": {
                    "url": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                }
              }
            },
            "picture": {
              "properties": {
                "url": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "product_order": {
              "type": "long"
            }
          }
        },
        "characteristics": {
          "type": "nested",
          "properties": {
            "boolean_value": {
              "type": "boolean"
            },
            "context": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "enum_value": {
              "type": "keyword"
            },
            "environment": {
              "type": "keyword"
            },
            "id": {
              "type": "long"
            },
            "is_exclusion": {
              "type": "boolean"
            },
            "max_value": {
              "type": "float"
            },
            "min_value": {
              "type": "float"
            },
            "name": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "symbol": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "technical_branch_id": {
              "type": "long"
            },
            "translations": {
              "properties": {
                "bg": {
                  "properties": {
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "cn": {
                  "properties": {
                    "enum_value": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "unit": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "cs": {
                  "properties": {
                    "enum_value": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "de": {
                  "properties": {
                    "enum_value": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "unit": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "en": {
                  "properties": {
                    "enum_value": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "unit": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "es": {
                  "properties": {
                    "enum_value": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "unit": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "fr": {
                  "properties": {
                    "enum_value": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "unit": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "gr": {
                  "properties": {
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "unit": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "hr": {
                  "properties": {
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "it": {
                  "properties": {
                    "enum_value": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "unit": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "ne": {
                  "properties": {
                    "enum_value": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "unit": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "pl": {
                  "properties": {
                    "enum_value": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "unit": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "po": {
                  "properties": {
                    "enum_value": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "unit": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "ro": {
                  "properties": {
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "ru": {
                  "properties": {
                    "enum_value": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "unit": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "sk": {
                  "properties": {
                    "enum_value": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                }
              }
            },
            "type": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "unit": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            }
          }
        },
        "comment": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "cpm_machines": {
          "type": "long"
        },
        "cpm_pieces": {
          "type": "long"
        },
        "cpp_accessories": {
          "type": "long"
        },
        "cpp_pieces": {
          "type": "long"
        },
        "customs_code": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "d3e": {
          "properties": {
            "company_id": {
              "type": "long"
            },
            "id": {
              "type": "long"
            },
            "name": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "price": {
              "type": "float"
            }
          }
        },
        "documents": {
          "type": "nested",
          "properties": {
            "environment": {
              "type": "keyword"
            },
            "file": {
              "properties": {
                "file": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "folder": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "size": {
                  "type": "long"
                },
                "type": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "url": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "id": {
              "type": "long"
            },
            "language_id": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "name": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "order": {
              "type": "long"
            },
            "type_id": {
              "type": "long"
            }
          }
        },
        "environment": {
          "type": "keyword"
        },
        "extensions": {
          "dynamic": "true",
          "properties": {
            "22": {
              "properties": {
                "images": {
                  "type": "long"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "ACCOUNT": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "has_forced_price": {
                  "type": "boolean"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "price": {
                  "type": "float"
                },
                "price_taxed": {
                  "type": "float"
                },
                "reference": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "score": {
                  "type": "integer"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "ACCOUNT_TERACT": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "has_forced_price": {
                  "type": "boolean"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "reference": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "score": {
                  "type": "integer"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "ALL PRODUCT": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "APP_COLLECT_FEIDER": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "BUILDER": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "BUILDER BOB": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "BUILDER_MARKETPLACES": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "BUILDER_POLOGNE": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "price": {
                  "type": "float"
                },
                "price_taxed": {
                  "type": "float"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "specificities": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "url": {
                  "type": "keyword"
                }
              }
            },
            "CAPITOOLS": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "CAPITOOLS_SHOP": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "discount_price": {
                  "type": "float"
                },
                "discount_price_taxed": {
                  "type": "float"
                },
                "has_forced_price": {
                  "type": "boolean"
                },
                "images": {
                  "type": "long"
                },
                "img": {
                  "properties": {
                    "file": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "folder": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "size": {
                      "type": "long"
                    },
                    "type": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "url": {
                      "type": "keyword"
                    }
                  }
                },
                "is_visible": {
                  "type": "boolean"
                },
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "price": {
                  "type": "float"
                },
                "price_taxed": {
                  "type": "float"
                },
                "reference": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "specificities": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "url": {
                  "type": "keyword"
                }
              }
            },
            "CATMAN TEST": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "CHIPPERFIELD": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "COLLECTION_TRACTEUR": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "has_forced_price": {
                  "type": "boolean"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "price": {
                  "type": "float"
                },
                "price_taxed": {
                  "type": "float"
                },
                "reference": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "score": {
                  "type": "integer"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "specificities": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "url": {
                  "type": "keyword"
                }
              }
            },
            "COLLECTION_TRACTEUR_ENVIRONMENT": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "DASH_CENTRALES": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "DASH_FOURNISSEURS": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "EXPORT ARBO": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "FEIDER": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "FEIDER_VITRINE": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "custom_fields": {
                  "properties": {
                    "affiliate_link_amazon_fr": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "affiliate_link_manomano_fr": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "HYUNDAI": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "HYUNDAI_FRANCE": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "custom_fields": {
                  "properties": {
                    "affiliate_link_amazon_fr": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "affiliate_link_manomano_fr": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "images": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "HYUNDAI_POLOGNE": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "discount_price": {
                  "type": "float"
                },
                "discount_price_taxed": {
                  "type": "float"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "price": {
                  "type": "float"
                },
                "price_taxed": {
                  "type": "float"
                },
                "score": {
                  "type": "integer"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                },
                "url": {
                  "type": "keyword"
                }
              }
            },
            "MARKETPLACE": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "custom_fields": {
                  "properties": {
                    "Autopropulsé": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Avec_disjoncteur_thermique ": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Capacite_de_reservoir_en_L": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Diamètre maximum de forage": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Diamètre_minimum_de_forage": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Débrayage de lame": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Décompresseur_(thermique) ": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Guidon_réglable_en_hauteur": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Hauteur_maximale_de_coupe_en_mm": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Hauteur_minimale_de_coupe_en_mm": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Intégré_à_une_plateforme": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Matière de la lame": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Matière-produit": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Matière_lame": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Mécanisme_de_verrouillage": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Orientable": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Pente maximum conseillée (en %)": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Pression_bar": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Réglage_de_la_hauteur_de_coupe": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Système_de_coupe": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Transmission": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Tube extensible": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Type de couteau": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Type_d_avance_du_fil ": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Type_de_batterie": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Type_de_lame": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Type_de_propulsion": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Type_de_terrain": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "Témoin_de_remplissage_du_bac": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "capacite_de_collecte": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "cm_mm": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "cv": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "m3_par_minute": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "mm_cm": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "noise_level": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "power_w": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "pression_hydraulique_max_Mpa": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "usage_du_produit": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "vitesse_de_rotation": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "voltage": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "discount_price": {
                  "type": "float"
                },
                "discount_price_taxed": {
                  "type": "float"
                },
                "forced_sale_duration": {
                  "type": "long"
                },
                "has_forced_price": {
                  "type": "boolean"
                },
                "images": {
                  "type": "long"
                },
                "img": {
                  "properties": {
                    "file": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "folder": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "size": {
                      "type": "long"
                    },
                    "type": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "url": {
                      "type": "keyword"
                    }
                  }
                },
                "is_visible": {
                  "type": "boolean"
                },
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "price": {
                  "type": "float"
                },
                "price_taxed": {
                  "type": "float"
                },
                "reference": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "score": {
                  "type": "integer"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "specificities": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "url": {
                  "type": "keyword"
                },
                "videos": {
                  "type": "long"
                }
              }
            },
            "MOWDIRECT": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "has_forced_price": {
                  "type": "boolean"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "reference": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "score": {
                  "type": "integer"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "specificities": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "SANDBOX": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "SWAP": {
              "properties": {
                "average_rating": {
                  "type": "float"
                },
                "currency_id": {
                  "type": "long"
                },
                "custom_fields": {
                  "properties": {
                    "HP": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "default_category_id": {
                  "type": "long"
                },
                "discount_end_date": {
                  "properties": {
                    "date": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "timezone": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "timezone_type": {
                      "type": "long"
                    }
                  }
                },
                "discount_price": {
                  "type": "float"
                },
                "discount_price_taxed": {
                  "type": "float"
                },
                "discount_start_date": {
                  "properties": {
                    "date": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "timezone": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "timezone_type": {
                      "type": "long"
                    }
                  }
                },
                "forced_sale_duration": {
                  "type": "long"
                },
                "has_forced_price": {
                  "type": "boolean"
                },
                "images": {
                  "type": "long"
                },
                "img": {
                  "properties": {
                    "file": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "folder": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "size": {
                      "type": "long"
                    },
                    "type": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "url": {
                      "type": "keyword"
                    }
                  }
                },
                "is_visible": {
                  "type": "boolean"
                },
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "price": {
                  "type": "float"
                },
                "price_taxed": {
                  "type": "float"
                },
                "reference": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "review_count": {
                  "type": "long"
                },
                "score": {
                  "type": "integer"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "specificities": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "url": {
                  "type": "keyword"
                },
                "videos": {
                  "type": "long"
                }
              }
            },
            "SWAP_ENVIRONMENT": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "SWAP_RUSSIE": {
              "properties": {
                "average_rating": {
                  "type": "float"
                },
                "currency_id": {
                  "type": "long"
                },
                "has_forced_price": {
                  "type": "boolean"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "price": {
                  "type": "float"
                },
                "price_taxed": {
                  "type": "float"
                },
                "reference": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "review_count": {
                  "type": "long"
                },
                "score": {
                  "type": "integer"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "SWAP_SERVICES": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "has_forced_price": {
                  "type": "boolean"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "reference": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "score": {
                  "type": "integer"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "SWAP_SPAREKA_2": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "has_forced_price": {
                  "type": "boolean"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "price": {
                  "type": "float"
                },
                "price_taxed": {
                  "type": "float"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "SWAP_TEST": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "has_forced_price": {
                  "type": "boolean"
                },
                "images": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "reference": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "specificities": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "url": {
                  "type": "keyword"
                }
              }
            },
            "TERACT_ENVIRONMENT": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "TERACT_SHOP": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "default_category_id": {
                  "type": "long"
                },
                "forced_sale_duration": {
                  "type": "long"
                },
                "has_forced_price": {
                  "type": "boolean"
                },
                "img": {
                  "properties": {
                    "file": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "folder": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "size": {
                      "type": "long"
                    },
                    "type": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "url": {
                      "type": "keyword"
                    }
                  }
                },
                "is_visible": {
                  "type": "boolean"
                },
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "price": {
                  "type": "float"
                },
                "price_taxed": {
                  "type": "float"
                },
                "reference": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "score": {
                  "type": "integer"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "url": {
                  "type": "keyword"
                }
              }
            },
            "TEST_FERDINAND": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "has_forced_price": {
                  "type": "boolean"
                },
                "images": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "price": {
                  "type": "float"
                },
                "price_taxed": {
                  "type": "float"
                },
                "reference": {
                  "type": "keyword",
                  "fields": {
                    "text": {
                      "type": "search_as_you_type",
                      "doc_values": "false",
                      "max_shingle_size": 3,
                      "analyzer": "folding_analyzer"
                    }
                  }
                },
                "score": {
                  "type": "integer"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "specificities": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "UK_ENVIRONMENT": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                }
              }
            },
            "VENTE_RECONDITIONNES": {
              "properties": {
                "currency_id": {
                  "type": "long"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "search_title": {
                  "type": "text",
                  "analyzer": "search_french"
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "specificities": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            }
          }
        },
        "hs_code": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "id": {
          "type": "long"
        },
        "image": {
          "properties": {
            "file": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "folder": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "size": {
              "type": "long"
            },
            "type": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "url": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            }
          }
        },
        "images": {
          "type": "nested",
          "properties": {
            "environment": {
              "type": "keyword"
            },
            "file": {
              "properties": {
                "file": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "folder": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "size": {
                  "type": "long"
                },
                "type": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "url": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "id": {
              "type": "long"
            },
            "language_id": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "title": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "type": {
              "type": "long"
            }
          }
        },
        "in_stock": {
          "type": "boolean"
        },
        "is_obsolete": {
          "type": "boolean"
        },
        "is_visible": {
          "type": "boolean"
        },
        "long_description": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "machine": {
          "properties": {
            "buying_price": {
              "type": "float"
            },
            "cegid_d_p_r": {
              "type": "float"
            },
            "exploded_view": {
              "properties": {
                "file": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "folder": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "size": {
                  "type": "long"
                },
                "type": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "url": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "id": {
              "type": "long"
            },
            "is_motor": {
              "type": "boolean"
            },
            "is_repair_forbidden": {
              "type": "boolean"
            },
            "max_return_rate": {
              "type": "float"
            },
            "observed_public_price": {
              "type": "float"
            },
            "permanent_p_p_i": {
              "type": "float"
            },
            "pricing_discount_a": {
              "type": "float"
            },
            "pricing_discount_a_a": {
              "type": "float"
            },
            "pricing_discount_b": {
              "type": "float"
            },
            "pricing_discount_c": {
              "type": "float"
            },
            "real_d_p_r": {
              "type": "float"
            },
            "repair_score": {
              "type": "long"
            },
            "return_rate": {
              "type": "float"
            },
            "supplier_id": {
              "type": "long"
            },
            "supplier_reference": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "universal_branch": {
              "properties": {
                "alias": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "alias_slugified": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "id": {
                  "type": "long"
                },
                "name": {
                  "type": "search_as_you_type",
                  "doc_values": "false",
                  "max_shingle_size": 3,
                  "analyzer": "folding_analyzer"
                },
                "parent": {
                  "properties": {
                    "alias": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "alias_slugified": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "id": {
                      "type": "long"
                    },
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "parent": {
                      "properties": {
                        "alias": {
                          "type": "text",
                          "fields": {
                            "keyword": {
                              "type": "keyword",
                              "ignore_above": 256
                            }
                          }
                        },
                        "alias_slugified": {
                          "type": "text",
                          "fields": {
                            "keyword": {
                              "type": "keyword",
                              "ignore_above": 256
                            }
                          }
                        },
                        "id": {
                          "type": "long"
                        },
                        "name": {
                          "type": "text",
                          "fields": {
                            "keyword": {
                              "type": "keyword",
                              "ignore_above": 256
                            }
                          }
                        },
                        "parent": {
                          "properties": {
                            "alias": {
                              "type": "text",
                              "fields": {
                                "keyword": {
                                  "type": "keyword",
                                  "ignore_above": 256
                                }
                              }
                            },
                            "alias_slugified": {
                              "type": "text",
                              "fields": {
                                "keyword": {
                                  "type": "keyword",
                                  "ignore_above": 256
                                }
                              }
                            },
                            "id": {
                              "type": "long"
                            },
                            "name": {
                              "type": "text",
                              "fields": {
                                "keyword": {
                                  "type": "keyword",
                                  "ignore_above": 256
                                }
                              }
                            },
                            "parent": {
                              "properties": {
                                "alias": {
                                  "type": "text",
                                  "fields": {
                                    "keyword": {
                                      "type": "keyword",
                                      "ignore_above": 256
                                    }
                                  }
                                },
                                "alias_slugified": {
                                  "type": "text",
                                  "fields": {
                                    "keyword": {
                                      "type": "keyword",
                                      "ignore_above": 256
                                    }
                                  }
                                },
                                "id": {
                                  "type": "long"
                                },
                                "name": {
                                  "type": "text",
                                  "fields": {
                                    "keyword": {
                                      "type": "keyword",
                                      "ignore_above": 256
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        },
        "machines": {
          "type": "nested",
          "properties": {
            "brand": {
              "properties": {
                "id": {
                  "type": "long"
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "id": {
              "type": "long"
            },
            "image": {
              "properties": {
                "url": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "name": {
              "type": "search_as_you_type",
              "doc_values": "false",
              "max_shingle_size": 3,
              "analyzer": "folding_analyzer"
            },
            "ref": {
              "type": "search_as_you_type",
              "doc_values": "false",
              "max_shingle_size": 3,
              "analyzer": "folding_analyzer"
            },
            "type": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "universal_branch_id": {
              "type": "long"
            },
            "url": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "weight": {
              "type": "float"
            }
          }
        },
        "meta_description": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "meta_title": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "name": {
          "type": "keyword",
          "fields": {
            "text": {
              "type": "search_as_you_type",
              "doc_values": "false",
              "max_shingle_size": 3,
              "analyzer": "folding_analyzer"
            }
          }
        },
        "original_references": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "packaging": {
          "properties": {
            "package_depth": {
              "type": "long"
            },
            "package_height": {
              "type": "long"
            },
            "package_length": {
              "type": "long"
            },
            "product_depth": {
              "type": "long"
            },
            "product_height": {
              "type": "long"
            },
            "product_length": {
              "type": "long"
            }
          }
        },
        "piece": {
          "properties": {
            "forced_sale_duration": {
              "type": "long"
            },
            "has_fixed_price": {
              "type": "boolean"
            },
            "has_forced_price": {
              "type": "boolean"
            },
            "id": {
              "type": "long"
            },
            "is_consumable": {
              "type": "boolean"
            },
            "is_highlighted": {
              "type": "boolean"
            },
            "is_origin": {
              "type": "boolean"
            },
            "swap_price": {
              "type": "float"
            },
            "technical_branch": {
              "properties": {
                "id": {
                  "type": "long"
                },
                "name": {
                  "type": "search_as_you_type",
                  "doc_values": "false",
                  "max_shingle_size": 3,
                  "analyzer": "folding_analyzer"
                },
                "parent": {
                  "properties": {
                    "id": {
                      "type": "long"
                    },
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "parent": {
                      "properties": {
                        "id": {
                          "type": "long"
                        },
                        "name": {
                          "type": "text",
                          "fields": {
                            "keyword": {
                              "type": "keyword",
                              "ignore_above": 256
                            }
                          }
                        },
                        "parent": {
                          "properties": {
                            "id": {
                              "type": "long"
                            },
                            "name": {
                              "type": "text",
                              "fields": {
                                "keyword": {
                                  "type": "keyword",
                                  "ignore_above": 256
                                }
                              }
                            },
                            "parent": {
                              "properties": {
                                "id": {
                                  "type": "long"
                                },
                                "name": {
                                  "type": "text",
                                  "fields": {
                                    "keyword": {
                                      "type": "keyword",
                                      "ignore_above": 256
                                    }
                                  }
                                },
                                "parent": {
                                  "properties": {
                                    "id": {
                                      "type": "long"
                                    },
                                    "name": {
                                      "type": "text",
                                      "fields": {
                                        "keyword": {
                                          "type": "keyword",
                                          "ignore_above": 256
                                        }
                                      }
                                    }
                                  }
                                },
                                "score": {
                                  "type": "long"
                                }
                              }
                            },
                            "score": {
                              "type": "long"
                            }
                          }
                        },
                        "score": {
                          "type": "long"
                        }
                      }
                    },
                    "score": {
                      "type": "long"
                    }
                  }
                },
                "score": {
                  "type": "long"
                }
              }
            }
          }
        },
        "pieces": {
          "type": "nested",
          "properties": {
            "brand": {
              "properties": {
                "id": {
                  "type": "long"
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "aliases": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
              }
            },
            "id": {
              "type": "long"
            },
            "image": {
              "properties": {
                "url": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "name": {
              "type": "search_as_you_type",
              "doc_values": "false",
              "max_shingle_size": 3,
              "analyzer": "folding_analyzer"
            },
            "ref": {
              "type": "search_as_you_type",
              "doc_values": "false",
              "max_shingle_size": 3,
              "analyzer": "folding_analyzer"
            },
            "swap_price": {
              "type": "float"
            },
            "technical_branch_id": {
              "type": "long"
            },
            "type": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "url": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "weight": {
              "type": "float"
            }
          }
        },
        "pricing": {
          "properties": {
            "5": {
              "type": "float"
            },
            "20": {
              "type": "float"
            },
            "27": {
              "type": "float"
            },
            "272": {
              "type": "float"
            },
            "287": {
              "type": "float"
            },
            "312": {
              "type": "float"
            },
            "314": {
              "type": "float"
            },
            "317": {
              "type": "float"
            },
            "327": {
              "type": "float"
            }
          }
        },
        "ref": {
          "type": "keyword",
          "fields": {
            "text": {
              "type": "search_as_you_type",
              "doc_values": "false",
              "max_shingle_size": 3,
              "analyzer": "folding_analyzer"
            }
          }
        },
        "refurbished": {
          "properties": {
            "grade": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "original_product": {
              "properties": {
                "barcode": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "best_image": {
                  "properties": {
                    "file": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "folder": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "size": {
                      "type": "long"
                    },
                    "type": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "url": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "brand": {
                  "properties": {
                    "id": {
                      "type": "long"
                    },
                    "label": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "name": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "comment": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "customs_code": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "hs_code": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "id": {
                  "type": "long"
                },
                "image": {
                  "properties": {
                    "file": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "folder": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "size": {
                      "type": "long"
                    },
                    "type": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "url": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    }
                  }
                },
                "is_obsolete": {
                  "type": "boolean"
                },
                "is_visible": {
                  "type": "boolean"
                },
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "machine": {
                  "properties": {
                    "buying_price": {
                      "type": "float"
                    },
                    "cegid_d_p_r": {
                      "type": "float"
                    },
                    "exploded_view": {
                      "properties": {
                        "file": {
                          "type": "text",
                          "fields": {
                            "keyword": {
                              "type": "keyword",
                              "ignore_above": 256
                            }
                          }
                        },
                        "folder": {
                          "type": "text",
                          "fields": {
                            "keyword": {
                              "type": "keyword",
                              "ignore_above": 256
                            }
                          }
                        },
                        "size": {
                          "type": "long"
                        },
                        "type": {
                          "type": "text",
                          "fields": {
                            "keyword": {
                              "type": "keyword",
                              "ignore_above": 256
                            }
                          }
                        },
                        "url": {
                          "type": "text",
                          "fields": {
                            "keyword": {
                              "type": "keyword",
                              "ignore_above": 256
                            }
                          }
                        }
                      }
                    },
                    "id": {
                      "type": "long"
                    },
                    "is_motor": {
                      "type": "boolean"
                    },
                    "is_repair_forbidden": {
                      "type": "boolean"
                    },
                    "max_return_rate": {
                      "type": "long"
                    },
                    "observed_public_price": {
                      "type": "float"
                    },
                    "permanent_p_p_i": {
                      "type": "float"
                    },
                    "pricing_discount_a": {
                      "type": "float"
                    },
                    "pricing_discount_a_a": {
                      "type": "float"
                    },
                    "pricing_discount_b": {
                      "type": "float"
                    },
                    "pricing_discount_c": {
                      "type": "float"
                    },
                    "real_d_p_r": {
                      "type": "float"
                    },
                    "repair_score": {
                      "type": "long"
                    },
                    "return_rate": {
                      "type": "long"
                    },
                    "supplier_id": {
                      "type": "long"
                    },
                    "supplier_reference": {
                      "type": "text",
                      "fields": {
                        "keyword": {
                          "type": "keyword",
                          "ignore_above": 256
                        }
                      }
                    },
                    "universal_branch": {
                      "properties": {
                        "alias": {
                          "type": "text",
                          "fields": {
                            "keyword": {
                              "type": "keyword",
                              "ignore_above": 256
                            }
                          }
                        },
                        "alias_slugified": {
                          "type": "text",
                          "fields": {
                            "keyword": {
                              "type": "keyword",
                              "ignore_above": 256
                            }
                          }
                        },
                        "id": {
                          "type": "long"
                        },
                        "name": {
                          "type": "text",
                          "fields": {
                            "keyword": {
                              "type": "keyword",
                              "ignore_above": 256
                            }
                          }
                        },
                        "parent": {
                          "properties": {
                            "alias": {
                              "type": "text",
                              "fields": {
                                "keyword": {
                                  "type": "keyword",
                                  "ignore_above": 256
                                }
                              }
                            },
                            "alias_slugified": {
                              "type": "text",
                              "fields": {
                                "keyword": {
                                  "type": "keyword",
                                  "ignore_above": 256
                                }
                              }
                            },
                            "id": {
                              "type": "long"
                            },
                            "name": {
                              "type": "text",
                              "fields": {
                                "keyword": {
                                  "type": "keyword",
                                  "ignore_above": 256
                                }
                              }
                            },
                            "parent": {
                              "properties": {
                                "alias": {
                                  "type": "text",
                                  "fields": {
                                    "keyword": {
                                      "type": "keyword",
                                      "ignore_above": 256
                                    }
                                  }
                                },
                                "alias_slugified": {
                                  "type": "text",
                                  "fields": {
                                    "keyword": {
                                      "type": "keyword",
                                      "ignore_above": 256
                                    }
                                  }
                                },
                                "id": {
                                  "type": "long"
                                },
                                "name": {
                                  "type": "text",
                                  "fields": {
                                    "keyword": {
                                      "type": "keyword",
                                      "ignore_above": 256
                                    }
                                  }
                                },
                                "parent": {
                                  "properties": {
                                    "alias": {
                                      "type": "text",
                                      "fields": {
                                        "keyword": {
                                          "type": "keyword",
                                          "ignore_above": 256
                                        }
                                      }
                                    },
                                    "alias_slugified": {
                                      "type": "text",
                                      "fields": {
                                        "keyword": {
                                          "type": "keyword",
                                          "ignore_above": 256
                                        }
                                      }
                                    },
                                    "id": {
                                      "type": "long"
                                    },
                                    "name": {
                                      "type": "text",
                                      "fields": {
                                        "keyword": {
                                          "type": "keyword",
                                          "ignore_above": 256
                                        }
                                      }
                                    },
                                    "parent": {
                                      "properties": {
                                        "alias": {
                                          "type": "text",
                                          "fields": {
                                            "keyword": {
                                              "type": "keyword",
                                              "ignore_above": 256
                                            }
                                          }
                                        },
                                        "alias_slugified": {
                                          "type": "text",
                                          "fields": {
                                            "keyword": {
                                              "type": "keyword",
                                              "ignore_above": 256
                                            }
                                          }
                                        },
                                        "id": {
                                          "type": "long"
                                        },
                                        "name": {
                                          "type": "text",
                                          "fields": {
                                            "keyword": {
                                              "type": "keyword",
                                              "ignore_above": 256
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "ref": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "type": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "url": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "weight": {
                  "type": "float"
                }
              }
            }
          }
        },
        "resupplies": {
          "type": "nested",
          "properties": {
            "piece_order_id": {
              "type": "long"
            },
            "qty": {
              "type": "long"
            },
            "warehouse_id": {
              "type": "long"
            }
          }
        },
        "search_aliases": {
          "type": "text",
          "analyzer": "search_french"
        },
        "short_description": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "stocks": {
          "type": "nested",
          "properties": {
            "available_stock": {
              "type": "long"
            },
            "id": {
              "type": "long"
            },
            "is_main": {
              "type": "boolean"
            },
            "physical_stock": {
              "type": "long"
            },
            "warehouse": {
              "properties": {
                "id": {
                  "type": "long"
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            }
          }
        },
        "suppliers": {
          "type": "nested",
          "properties": {
            "buying_price": {
              "type": "float"
            },
            "buying_price_usd": {
              "type": "long"
            },
            "currency_id": {
              "type": "long"
            },
            "exchange_rate": {
              "type": "long"
            },
            "id": {
              "type": "long"
            },
            "product_id": {
              "type": "long"
            },
            "supplier_id": {
              "type": "long"
            },
            "supplier_reference": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "update_date": {
              "properties": {
                "date": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "timezone": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "timezone_type": {
                  "type": "long"
                }
              }
            }
          }
        },
        "translations": {
          "properties": {
            "bg": {
              "properties": {
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "cn": {
              "properties": {
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "cs": {
              "properties": {
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "de": {
              "properties": {
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "en": {
              "properties": {
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "es": {
              "properties": {
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "fr": {
              "properties": {
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "gr": {
              "properties": {
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "hr": {
              "properties": {
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "hu": {
              "properties": {
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "it": {
              "properties": {
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "ne": {
              "properties": {
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "pl": {
              "properties": {
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "po": {
              "properties": {
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "ro": {
              "properties": {
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "ru": {
              "properties": {
                "long_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "sk": {
              "properties": {
                "meta_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "meta_title": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "name": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "original_references": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "short_description": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            }
          }
        },
        "tutorials": {
          "type": "nested",
          "properties": {
            "title": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "youtube_id": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            }
          }
        },
        "type": {
          "type": "keyword"
        },
        "url": {
          "type": "keyword"
        },
        "videos": {
          "type": "nested",
          "properties": {
            "environment": {
              "type": "keyword"
            },
            "id": {
              "type": "long"
            },
            "order": {
              "type": "long"
            },
            "title": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "url": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            }
          }
        },
        "weight": {
          "type": "float"
        }
      }
    } 
 }