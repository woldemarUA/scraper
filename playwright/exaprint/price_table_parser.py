from bs4 import BeautifulSoup
import pandas as pd

def parse_price_table(html):
    soup  = BeautifulSoup(html, 'html.parser')
    # product_attributes = soup.find_all('div', class_='ProductPageAttributesLine__StyledGroupWrapper-sc-4erg16-0')
    # # print(len(product_attributes))
    # price_table = soup.find('table', class_='PriceGridTable__StyledPriceTable-sc-x9occo-2')
    # print(price_table.get_text(strip=True))
    # Initialize lists to store data
    quantities = []
    economique_prices = []
    standard_prices = []
    delivery_dates = []

    # Extract delivery dates from the table header
    header_row = soup.find('tr', class_='PriceGridTable__StyledGridHeaderTableRow-sc-x9occo-7')
    for cell in header_row.find_all('td', class_='PriceGridTable__StyledTableHeaderDeliveryDate-sc-x9occo-10'):
        date_span = cell.find('span', {'data-testid': 'minDeliveryDate'})
        delivery_dates.append(date_span.text if date_span else '')

    # Loop through each data row in the table
    for row in soup.find_all('tr', id=lambda x: x and 'priceGridKey' in x):
        quantity_cell = row.find('div', {'data-testid': 'cell-quantity-to-order'})
        quantity = quantity_cell.text.strip() if quantity_cell else ''
        quantities.append(quantity)
        
        # Extract prices for each type (Economique and Standard)
        price_cells = row.find_all('span', {'data-testid': 'price-in-cell'})
        if price_cells:
            # The first price cell is for "Economique" and the second for "Standard"
            economique_prices.append(price_cells[0].text.strip() if price_cells[0] else '')
            standard_prices.append(price_cells[1].text.strip() if len(price_cells) > 1 else '')

    # Create a DataFrame and save it to an Excel file
    df = pd.DataFrame({
        'Quantity': quantities,
        # 'Economique Delivery Date': [delivery_dates[0]] * len(quantities),
        'Economique Price': economique_prices,
        # 'Standard Delivery Date': [delivery_dates[1]] * len(quantities),
        # 'Standard Price': standard_prices
    })

    # Save to Excel
    df.to_excel('price_table.xlsx', index=False)
    print("Data saved to price_table.xlsx")