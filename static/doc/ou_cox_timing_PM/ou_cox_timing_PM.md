## A Poisson Model of Timing Prediction Markets
In prediction markets actors trade contracts which pay out one dollar if some underlying event occurs and nothing otherwise. This allows us to interpret the market price as an estimate of the probability of that event occuring; these estimates turn out to be remarkably good. <a target="_blank" href="/binary-AI09">My previous post</a> contains a more gentle introduction to the topic. The non-emperical literature has largely been concerned with how to design prediction markets that are useful, e.g. for analysts or decisions makers. However, with the recent emergence of <a traget="_blank" href="https://www.kalshi.com">Kalshi</a> and <a target="_blank" href="https://www.polymarket.com">Polymarket</a>, who both host a large number of liquid markets on various topics, I argue that the time is ripe for treating prediction market contracts as financial instruments in their own right, using all the techniques developed for derivative pricing. 

Although the current market providers primarily make a profit from retail traders using their platforms for mere gambling, prediction markets are worth studying for three reasons. First, they provide analysts with robust probability estimates for a large range of events, which can inform more qualified decision making. Prediction markets also offer a novel opportunity to hedge specific exposures, especially policy-related risks. Good models of market volatility are needed to do this effectively. Finally, these markets should be of particular interest to statisticians, as they provide easily accessible input signals to more complex models. An unemployment model, for example, could account for uncertainty about future central bank policy by including relevant prediction market prices as exogenous variables.

The standard prediction market contract is based on a question of type "Will event X occur at time T?", e.g. "Will Trump win the U.S. presidential election (on election day)?". The price history for this market is shown in Figure 1.

<figure>
    <img src="static/doc/ou_cox_timing_PM/trump2024daily.svg"/>
    <figcaption>Figure 1: Yes-price of the outcome market "Will Trump Win the 2024 Presidential Election?".</figcaption>
</figure>

Since the winner of the election is not certain until election day, the market price remains far away from zero or one, until the market resolves with a discrete jump. In the following I distinguish between the *yes-price* of a market, which is the price of a contract which pays out if the underlying event occurs and the market resolves to *yes*, and the *no-price*, which is the price of a contract with the opposite pay-out structure. Both yes- and no-contracts are typically tradable. With the new prediction market platforms, another type of market have recently been popularized, based on questions of the type "Will event X occur before event T?". The outcome of some event is not in question here, but rather the timing. I call such markets *timing markets* to distinguish them from the standard *outcome markets*. Figure 2 shows the price history for the timing market "Khamenei out as Supreme Leader of Iran in 2025?". The large price increase in June corresponds to the U.S.-Israeli attacks. 

<figure>
    <img src="static/doc/ou_cox_timing_PM/khameiniOut2025.svg"/>
    <figcaption>Figure 2: Yes-price of the timing market "Khamenei out as Supreme Leader of Iran in 2025?".</figcaption>
</figure>

Although timing markets have been studied before — <a target="_blank" href="https://www.nber.org/system/files/working_papers/w9587/w9587.pdf">Leigh, Wolfers & Zitzewitz (2003)</a> and <a target="_blank" href="https://www.ubplj.org/index.php/jpm/article/view/790">Wörle (2013)</a> examined markets on the ousting of Saddam Hussein and Ghadaffi, respectively — the distinction between them and outcome markets have not yet been properly made. It has not been recognized that timing markets exhbit qualtitatively different behavior. If the underlying event does not occur, then *ceteris paribus* the yes-price of a timing market will tend to zero as the end date approaches. If the event occurs, this will instead manifest as a discrete jump to a price of one. Because of this convergence behavior, timing markets should not be modeled in the same way as outcome markets. In the previous post I examined a volatility model for outcome market prices proposed by <a target="_blank" href="https://dl.acm.org/doi/pdf/10.1145/15664.1566414">Archak and Ipeirotis (2009).</a> Here I will present a novel model of timing markets, based on supposing that the underlying event arrives with a doubly stochastic Poisson process driven by an Ornstein-Uhlenbeck intensity. We will evaluate this model on the Khamenei-market. <b>Spoiler warning:</b> it stumbles due to being too stationary.

### Pricing Timing Contracts
Consider a timing prediction market with end date $T$ and suppose that the underlying event (and with it market resolution) arrives by a Poisson process with intensity process $\\lambda\_t.$ Let $R$ denote the resolution time of the market. The no-price at time $t$ consistent with interpreting prices as probabilities is then 

$$\\pi\_t^{\\text{no}} = \\mathbb{P}\\left[ R> T | \\mathcal{F}\_t \\right] = \\mathbb{E}\\left[e^{-\\int\_t^T\\lambda\_s \\mathrm{d}s} | \\mathcal{F}\_t \\right],$$

where $\\pi\_t^{\\text{no}}$ is adapted to the filtration $\\mathcal{F}\_t$. I do not account for discounting of future pay-outs when calculating prices. Since most prediction markets do not last longer than a year, any discounting effect would be small. This exact setup is used in the so called *reduced form*-family of models for pricing defaultable bonds. A key benefit is that the pricing equation above is exactly the same as for a zero-coupon bond, with $\\lambda\_t$ representing a stochastic short rate. This allows us to use the vast number of bond models for also pricing timing prediction markets.

By imposing dynamics on the intensity process $\\lambda\_t$ we can derive properties of the market price. I will suppose that $\\lambda\_t$ follows a mean-reverting Ornstein-Uhlenbeck process with dynamics

$$\\mathrm{d}\\lambda\_t = -\\kappa(\\lambda\_t - \\mu)\\mathrm{d}t + \\sigma \\mathrm{d}W\_t, \\quad \\kappa,\\sigma>0$$

where $W\_t$ is a standard Wiener process. Note that the Ornstein-Uhlenbeck process is not prevented from becoming negative, which would result in invalid intensity values. We avoid this by clipping the process to never be less than zero during simulation. As a consequence, all results derived below are approximations of the model actually implemented, but with realistic parameter values I do not expect this to introduce an unacceptable error. This clipping could be avoided by instead letting the intensity $\\lambda\_t$ be a Cox-Ingersoll-Ross process. It is, however, harder to study analytically than the Ornstein-Uhlenbeck process. You will have to wait for me to finish my Master's thesis to see how that works out!

The Gaussian transition density of the Ornstein-Uhlenbeck process allows us to derive the dynamics of the price process. Solving the stochastic differential equation governing the intensity process yields

$$\\lambda \_s \\vert \\mathcal{F}\_t \\sim \\mathcal{N}\\left(\\mu + e^{-\\kappa (s-t)}(\\lambda\_t-\\mu ), \\frac{\\sigma^2}{2\\kappa }\\left[1-e^{-2\\kappa (s-t)} \\right]\\right) \\quad\\text{for}\\quad s\\in(t,T].$$

It follows that the distribution of the forward integral $\\int\_t^T \\lambda\_s \\mathrm{d}s$ conditional on $\\mathcal{F}\_t$ is also Gaussian and $\\pi\_t^{\\text{no}}$ is the expected value of a log-normal random variable. By applying Itô's lemma we get 

$$\,\\mathrm{d}\\pi^{\\text{no}}\_t = \\pi^{\\text{no}}\_t\\left[ \\mu +L\_1(\\log\\pi^{\\text{no}}\_t + L\_2) \\right]\,\\mathrm{d}t + \\pi^{\\text{no}}\_t \\frac{\\sigma (1 - e^{-\\kappa \\tau })}{\\kappa }\,\\mathrm{d}W\_t,$$

where $\\tau := T-t$ and 

$$L\_1 := \\frac{\\kappa }{e^{-\\kappa \\tau }-1}, \\quad L\_2:=\\mu \\tau -\\frac{V}{2},$$

$$V := \\frac{\\sigma ^2}{2\\kappa ^3}\\left( 2\\kappa \\tau +4e^{-\\kappa \\tau }-e^{-2\\kappa \\tau } - 3 \\right).$$

There is also an invertible relationship between the no-price $\\pi\_t^{\\text{no}}$ and intensity $\\lambda\_t$:

$$\\lambda\_t = \\mu + L\_1(\\log\\pi\_t^{\\text{no}} + L\_2).$$

Note that the drift term of the price dynamics is exactly $\\pi\_t^{\\text{no}}\\lambda\_t > 0$; timing market prices are not martingales, conditional on non-resolution, but instead drift towards a no-price of one. This is exactly what we observed in real timing markets. We also see that the relative volatility 

$$\\frac{\\mathrm{d}\\pi\_t^{\\text{no}}}{\\pi\_t^{\\text{no}}} = \\frac{\\sigma(1-e^{-\\kappa \\tau})}{\\kappa}$$

is decreasing as $t \\rightarrow T$. <a target="_blank" href="https://fairmodel.econ.yale.edu/ec438/kaplan1.pdf">Chen, Ingersoll and Kaplan (2008, speaking about outcome markets)</a> argue that price volatility in prediction markets arises from uncertainity and disagreement and among traders about how future events will affect the probability of the underlying event occuring. With less time for significant news to arrive, this uncertainty shrinks as the market nears its end data. Consequently, a prediction market price model should incorporate decreasing volatility.

<details>
<summary>A Note on Simulation</summary>
<p>
We can easily simulate from the above model by discretizing the price dynamics with an Euler-Maruyama scheme on a time grid $t=t_1, t_2, \dots, t_n = T$. This yields

$$\pi^{\text{no}}_{k+1} = \pi_k^{\text{no}} + \pi_k^{\text{no}}\Delta\left[\mu + L_1(\log\pi^{\text{no}}_k + L_2)\right] + \pi^{\text{no}}_k \frac{\sigma}{\kappa}(e^{-\kappa\tau}-1)Z$$

where $\Delta$ is the size of the time step and $Z \sim \mathcal{N}(0, \Delta)$. We write $\pi_k^{\text{no}} := \pi_{t_k}^{\text{no}} $. These dynamics are conditional on the market not resolving. Therefore, when simulating sample $k+1$ we first determine whether the market resolved in the time interval $[t_k, t_{k+1}]$, which approximately occurs with probability

$$1 - e^{-\lambda_k\Delta } = 1 - \pi_k^{-\Delta L_1}e^{-\Delta (\mu +L_1L_2)}.$$

This uses the approximation $\int_{t_k}^{t_{k+1}}\lambda_s\mathrm{d}s \approx \lambda_k\Delta$, with the same shorthand $\lambda_k := \lambda_{t_k}$ as for the price process. In hindsight, I realize that we could derive the exact transition by a  transformation of the Ornstein-Uhlenbeck density. <em>Numquam labor desinit.</em>
<br><br>
When simulating we wish to avoid prices implying a negative intensity $\lambda_t$. This occurs when

$$0 > \lambda_t = \mu + L_1(\log\pi_t + L_2) \iff \pi_t > e^{-(\mu / L_1 + L_2)}.$$

There are multiple ways to handle such samples. I have chosen to simply discard them and draw new ones until one is valid. This is equivalent to sampling conditional on $\lambda_t \geq 0$. By picking an intensity process that that is strictly non-negative this complication could be avoided entirely.
</p>
</details>

#### Parameter Estimation
With the price model specified, the next step is to figure out how to estimate its parameters. The Euler-Maruyama scheme derived in the previous section gives us an approximate transition probability density for the price process. We have that

$$\\pi^{\\text{no}}\_{k+1}\\mid \\pi^{\\text{no}}\_k \\sim 
\\mathcal{N}\\left(
\\pi^{\\text{no}}\_k
+ \\pi^{\\text{no}}\_k \\Delta
\\left[\\mu + L\_1\\left(\\log \\pi^{\\text{no}}\_k + L\_2\\right)\\right],
\;
\\frac{(\\pi^{\\text{no}}\_k)^2 \\sigma^2 \\Delta}{\\kappa^2}
\\left(e^{-\\kappa \\tau}-1\\right)^2
\\right).$$

This allows us to use the quasi-maximum likelihood estimator of the parameters. These estimates ought to be acceptable if the discretization does not introduce significant error. The mean-reversion strength $\\kappa$ enters the likelihood non-linearly through terms of the form $e^{-C\\kappa\\tau}$. Because of this it is difficult to identify, which makes the numerical quasi-likelihood maximization especially sensitive to initial values. In order to find good ones we first perform a partial optimization, letting $\\mu$ and $\\sigma$ be free, while fixing $\\kappa$. We do this for a grid of reasonable values of $\\kappa \\in (0, 5)$. The set of parameters resulting in the highest quasi-likelihood was then used as initial values for a full optimization of all three parameters simultaneously. To enforce positivity on $\\sigma$ and $\\kappa$, we optimize their logarithm.

### Looking at a Real Market

With both simulation and estimation procedures in place, we are ready to explore applications of the latent Poisson model. To demonstrate these, we will fit the model to the Khamenei-market shown in Figure 2. The above method yields the following parameter estimates, with Wald 95 %-confidence intervals:

$$\\hat{\\mu} = 0.69\,\, [0.57, 0.80], \\quad 
\\hat{\\sigma} = 2.85\,\, [2.59, 3.15], \\quad
\\hat{\\kappa} = 3.61\,\, [2.34, 5.56].$$

The Wald confidence intervals are based on a Gaussian approximation of the parameter distribution. This is appropriate only if these distributions are symmetric, which is not necessarily the case for a highly non-linear model such as this one. One could diagnose this by looking at the profile likelihoods of the parameters, and if more accurate error estimates are needed, use these to compute profile likelihood-based confidence intervals instead. Equipped with parameter estimates, we can utilize the fitted model in various ways.

#### Reconstructing Intensity and Volatility
Recall that we have closed expressions for both the intensity and the volatility $v\_t$ in terms of the no-price $\\pi\_t^{\\text{no}}$:

$$\\lambda\_t = \\mu + L\_1(\\log\\pi\_t^{\\text{no}} + L\_2),\\quad v\_t = \\frac{\\pi\_t^{\\text{no}} \\sigma}{\\kappa}(1-e^{-\\kappa\\tau}).$$

This allows us to reconstruct intensity and volatility series from historic prices, given parameter estimates. Such reconstructions for the market "Khamenei out as Supreme Leader of Iran in 2025?" are shown in Figure 3. As expected, we see a spike in intensity coinciding with the increased yes-price in June. The corresponding change in the volatility is negative, because it is proportional to the no-price. The reconstructed volatility is plotted alongside the unsmoothed realized volatility, which is a very noisy estimator. The fact that the reconstruction is consistently higher than the realized volatility, except for during the spike when it is considerably lower is a first indication that our model does not capture the full volatility dynamics of market prices.

<figure>
    <img src="static/doc/ou_cox_timing_PM/reconstruction.svg"/>
    <figcaption> Figure 3: Intensity and volatility series reconstructed from historic prices for the market "Khamenei out as Supreme Leader of Iran in 2025?".</figcaption>
</figure>

#### Monte Carlo Forecasts

The fitted model does not only allow us to reconstruct historic intensity and volatility, but also to forecast future values. The simplest way to do this is to simulate the process a large number of time from some starting price. These Monte Carlo samples then approximate the model-implied distribution of future prices. Such forecasts, conditional on the market not resolving, are shown in Figure 4, from 6 September until the end of 2025, together with 95 % confidence intervals. I ran 1 000 Monte Carlo simulations. To avoid data leakage, the model parameters were re-estimated with data only available up until that time. The new parameters (with 95 % Wald confidence intervals)

$$\\hat{\\mu} = 0.83\;[0.75,\,0.92], \\quad
\\hat{\\sigma} = 20.60\;[19.72,\,21.53], \\quad
\\hat{\\kappa} = 27.81\;[25.93,\,29.83]$$

were significantly different from the ones estimated on the full data. This is another indication that the estimation procedure described above is inadequate. Reconstructed intensities and volatilities using both sets of parameters are included in the figure.

<figure>
    <img src="static/doc/ou_cox_timing_PM/forecasts.svg"/>
    <figcaption>
    Figure 4: Monte Carlo forecasts of market price, intensity and volatility ($n=1000$) using only data available at the forecasting time 6 September. Confidence intervals are derived from the empirical quantiles of the Monte Carlo samples. Reconstructed intensity and volatility series, derived from parameters estimated on both the full and partial data, are included.
    </figcaption>
</figure>

The price forecasts are remarkably accurate. Note that although the level of the volatility forecast is very different from the reconstruction, due to the large difference in parameter estimates from the full and partial data, the dynamics seem to be well-captured. The Monte Carlo simulations used to produce these forecasts are conditioned on the market not resolving within the forecast horizon; the same methodology can also be used to get fine-grained estimates of when the market will resolve.

#### Fine-Grained Prediction of Resolution Probability

Consider a timing market with end date $T$ and denote its resolution time by $R \\leq T$. At some time $t\_0 < R$, the probability that the market will resolve before some later time $t\_1>t\_0$ is

$$\\mathbb{P}[R \\leq t\_1 | \\mathcal{F}\_{t\_0}] = 1-\\mathbb{E}\\left[e^{-\\int\_{t\_0}^{t\_1}\\lambda\_s\\mathrm{d}s}\\vert\\mathcal{F}\_{t\_0}\\right].$$

Under the assumed model, we can estimate this probability by simulating a large number of markets, starting at $\\pi\_{t\_0}^{\\text{no}}$, and simply counting the proportion of markets which resolve before time $t\_1$. Figure 5a contains these estimates for a range of horizons $t\_1-t\_0$ on simulated data. (It is possible to calculate this exactly, as a function of the current price and model parameters, but I realized this late.) Note that the probability of the market resolving before $t\_1$ converges to the yes-price $\\pi\_{t\_0}^{\\text{yes}}$ at time $t\_0$ as $t\_1 \\rightarrow T$. This corresponds to the probability estimates approaching the grey horizontal line. Figure 5b shows these estimates from the market "Khamenei out as Supreme Leader of Iran in 2025?", using parameters estimated from data available at time $t\_0 = $ 6 September. These estimates do not converge to the market price $\\pi\_{t\_0}^{\\text{yes}}$; many more simulations resolve than is expected given the market price. This indicates a serious misscalibration of the model. In order to pin down this issue, we will next consider a number of ways to evaluate model performance.

<figure>
    <div style="display: flex; gap: 20px;">
        <div style="flex: 1;">
            <img src="static/doc/ou_cox_timing_PM/prob_sim.svg" style="width: 100%;"/>
            <figcaption style="font-size: 0.9em; margin-top: 10px; text-align: center;">
                (a) Simulated data
            </figcaption>
        </div>
        <div style="flex: 1;">
            <img src="static/doc/ou_cox_timing_PM/prob_real.svg" style="width: 100%;"/>
            <figcaption style="font-size: 0.9em; margin-top: 10px; text-align: center;">
                (b) Real data 
            </figcaption>
        </div>
    </div>
    <figcaption>
        Figure 5: Estimated probability of resolving within a horizon from time $t_0 = 6$ September for (a) well-calibrated simulated data and (b) real data from the market "Khameini out as Supreme Leader of Iran in 2025?"
    </figcaption>
</figure>

#### Goodness-of-Fit
The approximate transition density derived above gives us a one-step prediction distribution, conditional on the market not resolving. Consider the residuals $r\_{k+1} := \\pi\_{k+1}^{\\text{no}} - \\pi\_k^{\\text{no}}$. The model implies that they have a conditional distribution

$$r\_{k+1}|\\pi\_k^{\\text{no}} \\sim 
\\mathcal{N}\\left(
\\pi^{\\text{no}}\_k \\Delta
\\left[\\mu + L\_1\\left(\\log \\pi^{\\text{no}}\_k + L\_2\\right)\\right],
\;
\\frac{(\\pi^{\\text{no}}\_k)^2 \\sigma^2 \\Delta}{\\kappa^2}
\\left(e^{-\\kappa \\tau}-1\\right)^2
\\right).$$

If the latent Poisson model fits the data well, then the standardized residuals ought to be uncorrelated and standard Gaussian-distributed. Figure 6 shows a histogram and quantile-quantile plot of the residuals. Their mean is -0.05 and their standard deviation is 1.17, which indicates good model fit. The distribution is symmetric with heavy tails, which is typical of financial time series. The figure also contains autocorrelation functions of the residuals and their squares. Although it is not definitive, they indicate that some correlation remains which the model has not accounted for. Note that this is in-sample validation, since the parameter estimates used to make one-step predictions are fitted to the entire price series. A more systematic evaluation of this model would have to include out-of-sample validation on multiple markets. 

<figure>
    <img src="static/doc/ou_cox_timing_PM/diagnostics.svg"/>
    <figcaption>
       Figure 6: Histogram, quantile-quantile plot, and autocorrelation function of standardized residuals and their squares. The one-step prediction residuals were computed from the market "Khamenei out as Supreme Leader of Iran in 2025?".
   </figcaption>
</figure>

We can get a closer look at how well the model predicts price volatility by considering the coverage of prediction intervals. The Gaussian one-step prediction distribution allows us to easily construct approximate prediction intervals for various confidence levels. If the model is well-calibrated, then an $\\alpha$-level prediction interval should contain the true value a fraction $\\alpha$ of the time. We can compute this coverage fraction across the entire price history for a range of confidence levels. This is done in Figure 7. Ideal model calibration would manifest as a diagonal line in such a plot. Instead, we see that the latent Poisson model systematically implies prediction intervals that are too wide, corresponding to an overestimation of the volatility. This agrees with what we observed when comparing the reconstructed volatility with the realized volatility in Figure 3. I believe that this is caused by the large price spike in June 2025. The true price volatility increased, as is seen in the realized volatility, which the stationary latent Poisson model could not accommodate. Instead, this caused the quasi-maximum likelihood estimator to inflate the baseline volatility of the entire price series, leading to the overestimation we observe. If this interpretation is correct, then the model could be improved by incorporating a non-stationary component. This could, for example, be a jump-term in the intensity-dynamics or time-varying parameters.

<figure>
    <img src="static/doc/ou_cox_timing_PM/ci_coverage.svg"/>
    <figcaption>
        Figure 7: Empirical coverage of Gaussian one-step prediction intervals for the market "Khamenei out as Supreme Leader of Iran in 2025?" plotted against nominal coverage, with the diagonal indicating perfect calibration.
    </figcaption>
</figure>

### An Insufficient but Promising Framework

I here present the first attempt, to the best of my knowledge, to model the price dynamics of timing prediction markets. By letting market resolution be driven by a latent Poisson process with stochastic intensity, the model reproduces the convergence behavior of real timing markets. Although I have presented a general framework, it is simple to adapt it to the prediction of specific markets, e.g. by incorporating external inputs driving the intensity process.

 While the model captures the qualitative behavior of timing markets, it is too simple to make good forecasts. It consistently overestimates the price volatility of the market we have studied and simulations resolve significantly more often than the real market price implies. I believe that the key flaw of the model is its stationarity. By adding a time-varying component, the model would be better able to adapt to the dynamics of real market prices. This could be done by letting parameters vary with time using a particle filter, by adding a jump-component to the price dynamics, or by including a Heston-style stochastic volatility. More work in this direction is to come, as I write my Master's thesis. 


*Published in February 2026. This work was originally done as a final project for a course on non-linear timeseries analysis at Lund University.*
