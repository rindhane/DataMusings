#file contains those utility functions which are 
#required for analysis of data.

def price_demand(df):
  ans=list()
  tmp=data[['price','number_of_reviews_ltm']].apply(
      lambda col: [col['price']]*int(col['number_of_reviews_ltm']),axis=1 )
  for i in tmp:
    ans.extend(i)
  return pd.Series(ans)