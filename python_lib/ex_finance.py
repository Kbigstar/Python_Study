# pip install -U finance-datareader
# pip install matplotlib
# pip install plotly
# pip install pandas

import FinanceDataReader as fdr
import matplotlib.pyplot as plt
AAPL = fdr.DataReader("AAPL")
AAPL['Close'].plot()
plt.show()