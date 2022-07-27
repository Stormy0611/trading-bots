/*
 * QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
 * Lean Algorithmic Trading Engine v2.0. Copyright 2014 QuantConnect Corporation.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
*/

using QuantConnect.Data.Market;

namespace QuantConnect.Indicators
{
    /// <summary>
    /// Volume Weighted Moving Average (VWMA) Indicator:
    /// It is calculated by adding up the dollars traded for every transaction (price multiplied
    /// by number of shares traded) and then dividing by the total shares traded for the day.
    /// </summary>
    public class VolumeWeightedMovingAverageIndicator : TradeBarIndicator, IIndicatorWarmUpPeriodProvider
    {
        /// <summary>
        /// In this VWMA calculation, typical price is defined by Close
        /// </summary>
        private readonly int _period;
        private readonly Identity _price;
        private readonly Identity _volume;
        private CompositeIndicator _vwma;

        /// <summary>
        /// Initializes a new instance of the VWMA class with the default name and period
        /// </summary>
        /// <param name="period">The period of the VWMA</param>
        public VolumeWeightedMovingAverageIndicator(int period)
            : this($"VWMA({period})", period)
        {
        }

        /// <summary>
        /// Initializes a new instance of the VWMA class with a given name and period
        /// </summary>
        /// <param name="name">string - the name of the indicator</param>
        /// <param name="period">The period of the VWMA</param>
        public VolumeWeightedMovingAverageIndicator(string name, int period)
            : base(name)
        {
            _period = period;

            _price = new Identity("Price");
            _volume = new Identity("Volume");

            // This class will be using WeightedBy indicator extension
            _vwma = _price.WeightedBy(_volume, period);
        }

        /// <summary>
        /// Gets a flag indicating when this indicator is ready and fully initialized
        /// </summary>
        public override bool IsReady => _vwma.IsReady;

        /// <summary>
        /// Required period, in data points, for the indicator to be ready and fully initialized.
        /// </summary>
        public int WarmUpPeriod => _period;

        /// <summary>
        /// Resets this indicator to its initial state
        /// </summary>
        public override void Reset()
        {
            _price.Reset();
            _volume.Reset();
            _vwma = _price.WeightedBy(_volume, _period);
            base.Reset();
        }

        /// <summary>
        /// Computes the next value of this indicator from the given state
        /// </summary>
        /// <param name="input">The input given to the indicator</param>
        /// <returns>A new value for this indicator</returns>
        protected override decimal ComputeNextValue(TradeBar input)
        {
            _price.Update(input.EndTime, GetTimeWeightedMovingAverage(input));
            _volume.Update(input.EndTime, input.Volume);
            return _vwma.Current.Value;
        }

        /// <summary>
        /// Gets an estimated average price to use for the interval covered by the input trade bar.
        /// </summary>
        /// <param name="input">The current trade bar input</param>
        /// <returns>An estimated average price over the trade bar's interval</returns>
        protected virtual decimal GetTimeWeightedMovingAverage(TradeBar input)
        {
            return input.Close;
        }
    }
}