"""All Message queue related configs, needs to be in sync with Magento."""

from kombu import Exchange

# OrderStatus
ORDER_STATE = Exchange(
    name='tendercuts.exchange.order.update',
    type='fanout',
    durable=True)
