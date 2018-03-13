class MultiSerializerMixin:
    """http://bit.ly/2p1HAkP"""
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerMixin, self).get_serializer_class()
