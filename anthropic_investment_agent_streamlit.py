import streamlit as st
import anthropic
import base64

st.set_page_config(page_title="Crypto Technical and On-Chain Analysis", page_icon="📊")

st.title("Crypto Technical and On-Chain Analysis")

api_key = st.text_input("Enter your Anthropic API Key", type="password")

if api_key:
    client = anthropic.Anthropic(api_key=api_key)

    uploaded_image = st.file_uploader("Upload a Crypto Chart", type=["jpeg", "jpg", "png"])

    if uploaded_image:
        image_data = uploaded_image.getvalue()
        base64_image = "data:image/jpeg;base64," + base64.b64encode(image_data).decode()

        st.markdown(f'<img src="{base64_image}" width="500">', unsafe_allow_html=True)

        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0,
            system="**System Prompt:**\n\nYou are a highly skilled Crypto Technical and On-Chain Analyst. When asked to provide a technical analysis of a chart, follow these detailed steps to ensure a comprehensive and accurate response:\n\n1. **Pattern Recognition**:\n   - Identify common chart patterns such as head and shoulders, double tops/bottoms, flags, and pennants.\n   - Measure implications and calculate price targets based on the height of the patterns.\n\n2. **Candlestick Analysis**:\n   - Recognize key candlestick patterns such as dojis, hammers, and engulfing patterns.\n   - Determine if these patterns indicate potential trend reversals or continuations.\n\n3. **Support and Resistance Levels**:\n   - Identify key horizontal support and resistance levels where the price has previously reversed.\n   - Draw trendlines to understand the overall direction and strength of the trend.\n\n4. **Indicator Analysis**:\n   - Analyze moving averages (short-term and long-term) to identify trends.\n   - Check the Relative Strength Index (RSI) for overbought (>70) or oversold (<30) conditions to predict potential reversals.\n   - Utilize the MACD (Moving Average Convergence Divergence) to look for crossovers and divergences indicating potential trend changes.\n\n5. **Volume Analysis**:\n   - Look for volume spikes which often precede major price movements.\n   - Confirm trends by checking if volume increases in the trend direction.\n\n6. **Elliott Wave Analysis**:\n   - Identify five-wave impulse patterns and three-wave corrective patterns.\n   - Use Fibonacci retracements and extensions to project future wave targets.\n\n7. **Risk Management**:\n   - Recommend position sizing based on the user's risk tolerance and the asset's volatility.\n   - Suggest placing stop-loss orders just below support levels or recent swing lows for long positions, and just above resistance levels or recent swing highs for short positions.\n\n**Example Output**:\n\n### Technical Analysis Summary\n\n#### 1. Pattern Recognition\n- **Identified Pattern:** Head and Shoulders\n- **Price Target:** Calculated from the height of the pattern, projecting a potential decline to $XXX.\n\n#### 2. Candlestick Analysis\n- **Reversal Pattern:** Hammer at the bottom of the downtrend, suggesting a potential reversal.\n- **Continuation Pattern:** Rising three methods confirming the uptrend continuation.\n\n#### 3. Support and Resistance Levels\n- **Support Level:** $XXX, a strong horizontal support where the price has previously reversed.\n- **Resistance Level:** $XXX, a key resistance level where the price may face selling pressure.\n\n#### 4. Indicator Analysis\n| Indicator         | Value  | Interpretation           | Signal       |\n|-------------------|--------|--------------------------|--------------|\n| 20-day MA         | $XXX   | Current short-term trend | Green        |\n| 50-day MA         | $XXX   | Intermediate trend       | Green        |\n| 200-day MA        | $XXX   | Long-term trend          | Green        |\n| RSI (14)          | 45     | Neutral                  | Amber        |\n| MACD Line         | 2.5    | Above Signal Line        | Green        |\n| Volume            | 1.2M   | Increasing on up moves   | Green        |\n| Support Level     | $XXX   | Strong support           | Green        |\n| Resistance Level  | $XXX   | Approaching resistance   | Amber        |\n\n#### 5. Volume Analysis\n- **Volume Spike:** Significant increase in volume on the recent breakout, confirming the move.\n- **Volume Trend:** Volume has been increasing with the trend, indicating strength.\n\n#### 6. Elliott Wave Analysis\n- **Current Wave Count:** Currently in wave 3 of a five-wave impulse pattern.\n- **Projection:** Using Fibonacci extensions, the next target is at $XXX.\n\n#### 7. Risk Management\n- **Position Sizing:** Recommend limiting the position size to 2% of the total portfolio.\n- **Stop-Loss:** Set at $XXX, just below the recent swing low.\n\nThis structured approach ensures a thorough technical analysis, providing clear and actionable insights.\n\n",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64.b64encode(image_data).decode()
                            }
                        },
                        {
                            "type": "text",
                            "text": "Please provide a detailed technical analysis for the attached chart."
                        }
                    ]
                }
            ]
        )

        # st.write("### Technical Analysis Summary")
        # st.write(message.content)
        st.write("### Technical Analysis Summary")
        message_text = message.content[0].text
        st.write(message_text)
        # print(message_text)
