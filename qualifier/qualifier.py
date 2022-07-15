import typing
from dataclasses import dataclass


@dataclass(frozen=True)
class Request:
    scope: typing.Mapping[str, typing.Any]

    receive: typing.Callable[[], typing.Awaitable[object]]
    send: typing.Callable[[object], typing.Awaitable[None]]


class RestaurantManager:
    def __init__(self):
        """Instantiate the restaurant manager.

        This is called at the start of each day before any staff get on
        duty or any orders come in. You should do any setup necessary
        to get the system working before the day starts here; we have
        already defined a staff dictionary.
        """
        self.staff = {}

    async def __call__(self, request: Request):
        """Handle a request received.

        This is called for each request received by your application.
        In here is where most of the code for your system should go.

        :param request: request object
            Request object containing information about the sent
            request to your application.
        """
        scope = request.scope
        if scope["type"] == "staff.onduty":
            self.staff[scope["id"]] = request

        elif scope["type"] == "staff.offduty":
            del self.staff[scope["id"]]

        elif scope["type"] == "order":
            speciality = scope["speciality"]
            for k, v in self.staff.items():
                if speciality in v.scope["speciality"]:
                    staff = self.staff[k]
                    break
            order = await request.receive()
            await staff.send(order)
            result = await staff.receive()
            await request.send(result)
