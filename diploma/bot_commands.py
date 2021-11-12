import help_user
import hello
import lowprice
import highprice
import bestdeal
import history
from typing import Dict

other_commands: Dict = {
    'Привет': hello.hello,
    '/hello-world': hello.hello,
    '/help': help_user.help_user,
    '/history': history.history,
}

commands: Dict = {
    '/lowprice': lowprice.LowPrice,
    '/highprice': highprice.HighPrice,
    '/bestdeal': bestdeal.BestDeal,
}
