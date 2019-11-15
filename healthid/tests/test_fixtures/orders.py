order = '''
mutation{{
  initiateOrder(
    name:"Important order",
    deliveryDate:"2019-05-30",
    productAutofill: true,
    supplierAutofill: true,
    destinationOutlet: {outlet_id}
  ){{
  order{{
      id
      orderNumber
      destinationOutlet{{
        id
      }}
  }}
  }}
  }}

'''
edit_order = '''
mutation{{
  editInitiatedOrder(
    orderId:{order_id},
    name:"Important order",
    deliveryDate:"2019-05-30",
    productAutofill: false,
    supplierAutofill: false,
    destinationOutletId: {outlet_id}
  ){{
  order{{
      id
      orderNumber
      destinationOutlet{{
        id
      }}
  }}
  }}
  }}

'''
suppliers_autofill = '''
mutation{{
  addOrderDetails(
    orderId: {order_id},
    products: [{product}]
  ){{
    message
    orderDetails{{
      id
      product{{
        id
      }}
      order{{
        id
        name
      }}
    }}
  }}
}}
'''

add_suppliers = '''
mutation{{
  addOrderDetails(
    orderId: {order_id},
    products: [{product}]
    suppliers: ["{supplier}"]
  ){{
    message
    orderDetails{{
      id
      product{{
        id
      }}
      order{{
        id
        name
      }}
      supplier{{
        id
      }}
    }}
  }}
}}
'''

add_quantities = '''
mutation{{
  addOrderDetails(
    orderId: {order_id},
    products: [{product}]
    quantities: [23]
  ){{
    message
    orderDetails{{
      id
      product{{
        id
      }}
      order{{
        id
        name
      }}
    }}
  }}
}}
'''

modify_order_quantities = '''
mutation{{
  addOrderDetails(
    orderId: {order_id},
    products: [{product}]
    quantities: [{quantity}]
  ){{
    message
    orderDetails{{
      id
      product{{
        id
      }}
    }}
    suppliersOrderDetails{{
      id
      orderDetails {{
        quantity
      }}
    }}
  }}
}}
'''

remove_order_detail = '''
mutation{{
  deleteOrderDetail(
    orderDetailId:"{order_detail_id}",
  ){{
     message
  }}
}}
'''

products_query = '''
query{
  productAutofill {
    id
    productName
    autofillQuantity
  }
}
'''

suppliers_order_details = '''
query {{
  suppliersOrderDetails(orderId: {order_id}){{
    id
    orderDetails {{
      product {{
        productName
      }}
      quantity
      supplier {{
        name
      }}
    }}
    supplierOrderName
    supplierOrderNumber
    deliverTo {{
      id
    }}
    deliveryDue
    additionalNotes
  }}
}}
'''

supplier_order_details = '''
query {{
  supplierOrderDetails(orderId: {order_id}, supplierId: "{supplier_id}"){{
    id
    orderDetails {{
      product {{
        productName
      }}
      quantity
      supplier {{
        name
      }}
    }}
    supplierOrderName
    supplierOrderNumber
    deliverTo {{
      id
    }}
    deliveryDue
    additionalNotes
  }}
}}
'''

approve_supplier_order = '''
mutation{{
  approveSupplierOrder(
    additionalNotes: "{additional_notes}",
    orderId: {order_id},
    supplierOrderIds: {supplier_order_ids}
    ){{
      message
      supplierOrderDetails {{
        id
        approved
      }}
    }}
  }}
'''

send_supplier_order_emails = '''
mutation{{
  sendSupplierOrderEmails(
    orderId: {order_id},
    supplierOrderIds: {supplier_order_ids}
    ){{
      message
    }}
  }}
'''

mark_supplier_order_as_sent = '''
mutation{{
  markSupplierOrderAsSent(
    orderId: {order_id},
    supplierOrderIds: {supplier_order_ids}
    ){{
      message
    }}
  }}
'''

retrieve_orders = '''
query {
  orders {
    id
  }
}
'''

retrieve_order = '''
query {{
  order(orderId: {order_id}) {{
    id
  }}
}}
'''

retrieve_open_orders = '''
query {
  openOrders {
    id
  }
}
'''

retrieve_closed_orders = '''
query {
  closedOrders {
    id
  }
}
'''

close_order = '''
mutation{{
  closeOrder(
    orderId:{order_id}
  ){{
    message
  }}
}}
'''

retrieve_orders_default_paginated = '''
query {
  orders {
    id
  }
  totalOrdersPagesCount
}
'''

retrieve_open_orders_default_paginated = '''
query {
  openOrders {
    id
    closed
  }
  totalOrdersPagesCount
}
'''

retrieve_closed_orders_default_paginated = '''
query {
  closedOrders {
    id
    closed
  }
  totalOrdersPagesCount
}
'''
retrieve_orders_custom_paginated = '''
query {{
  orders(pageCount:{pageCount} pageNumber: {pageNumber}) {{
    id
  }}
  totalOrdersPagesCount
}}
'''

retrieve_open_orders_custom_paginated = '''
query {{
  openOrders(pageCount:{pageCount} pageNumber: {pageNumber}) {{
    id
    closed
  }}
  totalOrdersPagesCount
}}
'''

retrieve_closed_orders_custom_paginated = '''
query {{
  closedOrders(pageCount:{pageCount} pageNumber: {pageNumber}) {{
    id
    closed
  }}
  totalOrdersPagesCount
}}
'''

auto_order = '''
query{
  autosuggestProductOrder{
    productName,
    suggestedQuantity
  }
}
'''
