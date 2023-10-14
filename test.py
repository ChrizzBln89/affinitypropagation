from valuationhub.valuationhub.assets import get_symbols, upload_quotes
import numpy as np

for x in np.arange(0, 300):
    try:
        df = upload_quotes(get_symbols())
        print(df)
    except:
        continue
