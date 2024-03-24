from .rest_adapter import RestAdapter
from .models import Result, Stops

test1 = RestAdapter()

result = test1.get("/stops/61127")
# print(type(result))
save = result.data
print(save['Name'])
