
create_stock_template_string = '''
        mutation{{
        createStockCountTemplate(
            productIds:{product_ids}
            assignedUserIds:{assigned_user_ids}
            designatedUserIds:{dessignate_user_ids}
            outletId:{outlet_id}
            eventId:{event_id}
        ){{
            stockTemplate{{
            id
            products{{
                pageInfo{{
                hasNextPage
                hasPreviousPage
                endCursor
                }}
                edges{{
                node{{
                    productName
                    id
                    unitCost
                }}
                }}
            }}
            assignedUsers{{
                    id
            }}
            designatedUsers{{
                id
                role{{
                name
                }}
            }}
            }}
            success
        }}
        }}
'''


edit_stock_template_string = '''
        mutation{{
        editStockCountTemplate(
            templateId:{template_id}
            productIds:{product_ids}
            assignedUserIds:{assigned_user_ids}
            designatedUserIds:{dessignate_user_ids}
            outletId:{outlet_id}
            eventId:{event_id}
        ){{
            stockTemplate{{
            id
            products{{
                pageInfo{{
                hasNextPage
                hasPreviousPage
                endCursor
                }}
                edges{{
                node{{
                    productName
                    id
                    unitCost
                }}
                }}
            }}
            assignedUsers{{
                    id
            }}
            designatedUsers{{
                id
                role{{
                name
                }}
            }}
            }}
            success
        }}
        }}
'''

delete_stock_template_string = '''
        mutation deleteTemplate{{
        deleteStockCountTemplate(templateId:{id}){{
            success
            errors
        }}
        }}
'''


query_all_templates = '''
        query {{
        stockTemplates(outletId:{outlet_id}) {{
            id
            assignedUsers {{
            id
            email
            }}
            designatedUsers {{
            id
            email
            }}
            createdAt
            outlet {{
            id
            name
            }}
            scheduleTime {{
            eventTitle
            description
            }}
            products{{
            edges{{
                node{{
                id
                productName
                }}
            }}
            }}
        }}
        }}

'''

query_single_template = '''
        query singleTemplate {{
        stockTemplate(templateId:{template_id}, outletId:{outlet_id}) {{
            id
            assignedUsers {{
            id
            email
            }}
            designatedUsers {{
            id
            email
            }}
            scheduleTime {{
            eventTitle
            description
            }}
            products {{
            edges {{
                node {{
                id
                productName
                }}
            }}
            }}
        }}
        }}

'''

initate_stock_count_query = '''
mutation initiateStock{{
  initiateStock(
    isCompleted:false,
    batchInfo: ["{batchInfo}"],
    product: {product},
    quantityCounted:[{quantityCounted}],
    remarks: "Don't ever tell me to count this stock again",
    stockTemplateId: {stockTemplateId},
    varianceReason: {varianceReason}
    specifyReason: "Was returned"
  ) {{
    errors
    message
    stockCount {{
      id
      varianceReason
      product {{
        id
        productName
      }}
      stockTemplate {{
        id
      }}
    }}
  }}
}}

'''

no_variance_reason_query = '''
mutation initiateStock{{
  initiateStock(
    isCompleted:false,
    batchInfo: ["{batchInfo}"],
    product: {product},
    quantityCounted:[{quantityCounted}],
    remarks: "Don't ever tell me to count this stock again",
    stockTemplateId: {stockTemplateId},
    varianceReason: {varianceReason}
    specifyReason: ""
  ) {{
    errors
    message
    stockCount {{
      id
      varianceReason
      createdAt
      updatedAt
      isCompleted
      isApproved
      product {{
        productName
        id
      }}
      stockTemplate {{
        id
        assignedUsers {{
          id
          email
        }}
      }}
    }}
  }}
}}
'''

update_stock_count_query = '''
  mutation {{
  updateStock (
    stockCountId:"{stockCountId}",
    batchInfo: ["{batchInfo}"],
    isCompleted: {isCompleted},
    product: {product},
    quantityCounted: [{quantityCounted}]
    varianceReason: Others
    specifyReason: "it expired"
  ){{
    message
    errors
    stockCount{{
      id
      varianceReason
      product {{
        id
        productName
      }}
       stockTemplate {{
        id
        assignedUsers {{
          id
          email
        }}
      }}
    }}
  }}
}}
'''

all_stock_counts = '''
query {
  stockCounts {
    id
    isApproved
    isCompleted
    varianceReason
  }
}
'''

single_stock_count = '''
query {{
  stockCount(id:"{stockCountId}") {{
    id
    isCompleted
    varianceReason
    product {{
      id
    }}
  }}
}}
'''

delete_stock_batch = '''
mutation {{
  removeBatchStock (
    batchInfo: "{batchInfo}",
    stockCountId: "{stockCountId}",
  ) {{
    message
    errors
    stockCount {{
      id
    }}
  }}
}}
'''
