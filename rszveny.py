import streamlit as st
import yfinance as yf
import ccxt
import pandas as pd
import datetime

def fetch_data(symbol, start_date, end_date, data_type):
    try:
        start_date = datetime.datetime.combine(start_date, datetime.datetime.min.time())
        end_date = datetime.datetime.combine(end_date, datetime.datetime.min.time())

        if data_type == "stock":
            data = yf.download(symbol, start=start_date, end=end_date)
        elif data_type == "crypto":
            exchange = ccxt.binance()  # !!!!Binance API!!!!
            ohlcv = exchange.fetch_ohlcv(symbol, '1d', since=start_date.timestamp() * 1000)
            data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
            data.set_index('timestamp', inplace=True)
            data = data[start_date:end_date]
        else:
            st.error("Érvénytelen adattípus. Válaszd ki a 'stock' vagy 'crypto' opciót.")
            return None

        return data
    except Exception as e:
        st.error(f"Hiba történt az adatok letöltése közben: {e}")
        return None

def main():
    st.title("Árfolyam Megjelenítő Alkalmazás")

    # Oldalsáv widgetek
    ticker_type = st.sidebar.selectbox("Válassz adattípust:", ["stock", "crypto"])
    symbol = st.sidebar.text_input("Szimbólum:")
    start_date = st.sidebar.date_input("Kezdő dátum:", datetime.date(2022, 1, 1))
    end_date = st.sidebar.date_input("Vég dátum:", datetime.date.today())

    if st.sidebar.button("Mutass adatokat"):
        if not symbol:
            st.warning("Kérlek, add meg a szimbólumot.")
        else:
            st.subheader(f"{symbol} {ticker_type} árfolyam ({start_date} - {end_date})")
            data = fetch_data(symbol, start_date, end_date, ticker_type)

            if data is not None and not data.empty:
                # Grafikon
                st.line_chart(data['Close'] if ticker_type == "stock" else data['close'])

                # Táblázat
                st.dataframe(data)

if __name__ == "__main__":
    main()
