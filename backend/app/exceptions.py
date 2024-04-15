class TicketAlreadyBookedError(Exception):
    """Already booked exception
    """
    def __init__(self, message="Ticket already booked"):
        self.message = message
        super().__init__(self.message)

class NoEventError(Exception):
    """Already booked exception
    """
    def __init__(self, message="Event does not exists"):
        self.message = message
        super().__init__(self.message)


