## Modeling Binary Prediction Markets
Who is going to win your country's next election? I'm sure you have som idea. You could probably also tell me something about how certain you are: "Almost certainly...", "I'm pretty sure...", "If I had to guess..." If I continued to press you and asked for a probability, say to the nearest percentage, then I bet you'd start to struggle. It's hard to quantify your beliefs like that! But I'd really like to know, so I'll offer you a bet. If party X wins the election I'll give you a dollar; if they lose you get nothing. What's the most money you'd be willing to pay to get in on this wager? It's easy to see that this amount implicitly reveals your degree of belief that party X will in fact win.

Bets such as these—or rather contracts which pay out to the holder in this manner—are traded in so called **prediction markets**. They were first introduced (in their modern form) by researchers at the University of Iowa to predict the 1988 U.S. presidential election. Interest has waxed and waned over the years; we are currently in a phase of high activity. Over a billion dollars was traded on the U.S. 2024 presidential election market on just the platform <a target="_blank" href="https://polymarket.com">Polymarket</a>, the current industry leader. 

Prediction markets have from the beginning attracted the attention of economists. There exists a deep literature on how these markets behave and how to design them. For example, it is well established that under reasonable conditions (including sufficient liquidity) the market price of a contract converges to the average belief of all traders, weighted by their trading budget. We also know that prediction market prices behave much like other financial time series, with uncorrelated returns, clustered volatility &c. 

Quite naturally, this strand of research is primarily interested in *constructing* markets that are *useful* for, say, informing policy makers. The models employed are typically based on market equilibria between many traders, with some distribution of beliefs about the event in question. Such models have delivered great theoretical insight, but are inherently limited by the fact that they are difficult to fit to real price data. 

A small number of authors have approached the problem at a higher level of abstraction. If we ignore the fine grain of market actors and transactions we are left with a time series and some knowledge of the process which generates it. Two properties are especially noteworthy:
<ol>
<li>Because a prediction market contract pays out a dollar at most, market prices are bounded between zero and one. No trader would willingly buy at a higher price.</li>
<li>As the market resolves, e.g. as the votes are counted on election day, the price goes to either zero or one, depending on the actual outcome of the underlying event.</li>
</ol>
You can see both of these in the below plot of the market price for the event "Will Trump win the 2024 U.S. Presidential election?":

<img style="width:100%;" class='figure' src="static/doc/binary_AI09/trump_price.svg"/>

While statisticians have developed many ways to model time series, these two constraints make prediction market prices unsuitable for the most common ones. As far as I have read, the best idea (at this level of abstraction) was had by NYU economists Nikolay Archak and Panagiotis G. Ipeirotis in their 2008 paper <a target="_blank" href="https://archive.nyu.edu/jspui/bitstream/2451/27716/4/CeDER-08-07.pdf">*Modeling Volatility in Prediction Markets*</a>. They model prediction market contracts as derivatives of unobservable **ability processes**. This is a theoretical construct, which represents the *ability* of either outcome to occur. 
### The Archak-Ipeirotis Model
Consider a **binary prediction market** with two possible outcomes, like a U.S. presidential election. Let $X\_1(t)$ and $X\_2(t)$ be the corresponding ability processes. Suppose also that the outcome is determined and the market resolves at time $t=T$, e.g. election day.

<details>
  <summary>Non-Ideal Market Resolution</summary>
  <p>
    In practice markets don't resolve instantly; it takes all of election day to determine the winner, for example. It is, however, common to assume away this detail by not looking at prices from the day of market resolution. The idea is that once the market begins to resolve the price process fundamentally changes. We cannot expect the same model to still work in this different regime. 
  </p>
</details>

We will assume that outcome one occurs if at time $t=T$
$$
X\_1(T) > X\_2(T)
$$
and *vice versa*. This resolution mechanism is ultimately what defines the ability processes. We will assume that the ability processes are continuous and that therefore the event $X\_1(T) = X\_2(T)$ occurs with probability zero. Under this model of how the market resolves, the rational price $\\pi\_1(t)$ at time $t$ of a contract which pays out one dollar if outcome one occurs is 
$$
\\pi\_1(t) = \\mathbb{P}\\left[ X\_1(T) > X\_2(T) \\vert \\mathcal{F}\_t \\right]  ,
$$
where we condition on a **filtration** $\\mathcal{F}\_t$. This loosely corresponds to accounting for all the information available at time $t$, including the values of $X\_1(t)$ and $X\_2(t)$. So far so good! To be able to compute this probability, Archak and Ipeirotis suppose that the ability processes satisfy the following **stochastic differential equations**:
$$
\\begin{align}
\\mathrm{d}X\_{1}(t) &= \\mu\_{1}(\\alpha X\_{1}(t) + \\beta) \\mathrm{d}t + \\sigma\_{1} (\\alpha X\_{1} + \\beta)\\mathrm{d}W\_{1}(t) \\\\\\\\
\\mathrm{d}X\_{2}(t) &= \\mu\_{2}(\\alpha X\_{2}(t) + \\beta) \\mathrm{d}t + \\sigma\_{2} (\\alpha X\_{2} + \\beta)\\mathrm{d}W\_{2}(t) \\\\
\\end{align}
$$
where the volatilities $\\sigma\_{1},\\sigma\_{2}>0$, $\\alpha>0$ and $\\mathbb{P}[\\alpha X\_{i} + \\beta>0] = 1$. Suppose that the Wiener processes $W\_1(t)$ and $W\_2(t)$ are correlated with correlation $\\rho$. This is a very general class of processes, which is almost (but not quite) a combination of the arithmetic and geometric Brownian motions. The graphs below show a simulation of these ability processes, with suitable parameter choices, together with a plot of their difference $X\_1(t) - X\_2(t)$:

<img style="width:100%;" class='figure' src="static/doc/binary_AI09/ability_processes.svg"/>

To calculate the price $\\pi\_1(t)$ we first transform the ability processes. Consider the function 
$$
f(X) = \\int\_{x\_0}^X \\frac{1}{\\alpha t+\\beta } \\,\\mathrm{d}t
$$
where $x\_0 \\in \\mathbb{R}$ is some starting point. This transformation is increasing in $X$ and therefore we have
$$
\\pi\_1(t) = \\mathbb{P}\\left[ X\_1(T) > X\_2(T) \\vert \\mathcal{F}\_t \\right]  = \\mathbb{P}\\left[ f(X\_1(T))>f(X\_2(T))\\vert \\mathcal{F}\_t \\right].  
$$
We are able to work out the distribution of $f(X\_i(T))\\vert\\mathcal{F}\_t$ for $i=1, 2$, which gives us a closed expression for the price $\\pi\_1(t)$ in terms of the ability difference process $\\Delta(t) := f(X\_1(t))-f(X\_2(t))$. It turns out that 
$$
\\pi \_1(t) = \\Phi\\left( \\frac{\\Delta (t) - \\tilde{\\mu }(T-t)}{\\tilde{\\sigma }\\sqrt{T-t}} \\right)  
$$
where $\\Phi$ is the cumulative distribution function of the standard Gaussian. The parameters 
$$
\\tilde{\\mu } := \\mu \_1 - \\mu\_2 + \\frac{\\alpha }{2}(\\sigma \_1^2 - \\sigma \_2^2) \\quad\\text{and}\\quad \\tilde{\\sigma } = \\sqrt{\\sigma\_1^2+\\sigma \_2^2-2\\rho }
$$
is the diffusion and volatility, respectively, of $\\Delta(t)$. 

<details>
  <summary>Proof for the interested reader</summary>
  <p>
    Put $Y_{i}(t) := f(X_{i}(t))$. We then have
    $$
    \pi_{1}(t) = \mathbb{P}[Y_{1}(T)>Y_{2}(T)\vert\mathcal{F}_{t}].
    $$
    By Itô's lemma
    $$
    \mathrm{d}Y_{i} = \frac{\partial f(X_{i})}{\partial X_{i} } \mathrm{d}X_{i} +\frac{1}{2}\frac{\partial^2f(X_{i})}{\partial X_{i}^2}(\mathrm{d}X_{i})^2
    $$
    where
    $$
    (\mathrm{d}X_{i})^2 = \sigma_{i}^2 (\alpha X_{i} + \beta)^2 \mathrm{d}t,
    $$
    $$
    \frac{\partial f(X_{i})}{\partial X_{i}} = \frac{1}{\alpha X_{i} + \beta}, \quad \frac{\partial^2 f(X_{i})}{\partial X_{i}^2} = - \frac{\alpha}{(\alpha X_{i} + \beta)^2}.
    $$
    Taking this together we get 
    $$
    \mathrm{d}Y_{i} = \mu_{i}\mathrm{d}t + \sigma_{i}\mathrm{d}W_{i} - \frac{\alpha\sigma_{i}^2}{2} \mathrm{d}t =\left( \mu_{i}  - \frac{\alpha\sigma_{i}^2}{2} \right) \mathrm{d}t + \sigma_{i}\mathrm{d}W_{i}.
    $$
    Put $\tilde{\mu}_{i} := \mu_{i} - \sigma_{i}^2\alpha/2$ and $\tau := T-t$. We then have
    $$
    Y_{i}(T)|\mathcal{F}_{t} = Y_{i}(t) + \tilde{\mu}_{i}\tau + \sigma_{i}\mathcal{N}(0, \tau) = \mathcal{N}\left( Y_{i}(t) + \tilde{\mu}_{i}\tau, \tau\sigma_{i}^2 \right)
    $$
    and 
    $$
    Y_{2}(T) - Y_{1}(T) | \mathcal{F}_{t} \sim \mathcal{N}\left( Y_{2}(t) - Y_{1}(t) + \tau(\tilde{\mu}_{2}- \tilde{\mu}_{1}), \tau(\sigma_{1}^2 + \sigma_{2}^2  -2\rho) \right).
    $$
    Let $\tilde{\sigma}^2 := \sigma_{1}^2 + \sigma_{2}^2 - 2\rho$. We finally get
    $$
    \pi_{1}(t) = \mathbb{P}[Y_{2}(T) - Y_{1}(T) < 0 | \mathcal{F}_{t}] = \Phi\left[\frac{\Delta(t) - \tau\tilde{\mu}}{\tilde{\sigma}\sqrt{\tau}}  \right]
    $$
    where $\Delta(t) := Y_{1}(t) - Y_{2}(t)$ and $\tilde{\mu} := \tilde{\mu}_{1} - \tilde{\mu}_{2}$. The difference process has the dynamics
    $$
    \mathrm{d}\Delta = \mathrm{d}Y_{1} - \mathrm{d}Y_{2} = \tilde{\mu}\mathrm{d}t + \tilde{\sigma}\mathrm{d}W.
    $$
  </p>
</details>

Ta-da! We have found a model of the market price in a binary prediction market:
$$\\begin{align}
\\,\\mathrm{d}\\Delta (t) &= \\tilde{\\mu }\\,\\mathrm{d}t + \\tilde{\\sigma } \\,\\mathrm{d}W(t) \\\\
\\pi \_1(t) &= \\Phi\\left( \\frac{\\Delta (t) - \\tilde{\\mu }(T-t)}{\\tilde{\\sigma }\\sqrt{T-t}} \\right)  
\\end{align}$$
By applying **Itô's lemma**—the chain rule of stochastic calculus—we can rewrite this in terms of the price alone:
$$
\\,\\mathrm{d}\\pi \_1(t)= \\frac{\\phi\\left( \\Phi ^{-1}[\\pi \_1(t)] \\right)}{\\sqrt{T-t}}\\,\\mathrm{d}W(t).
$$
where $\\varphi$ is the standard Gaussian density and $\\Phi^{-1}$ is the corresponding quantile function. Note that the price process has no drift term $\\mathrm{d}t$. That is, the Archak-Ipeirotis model implies that the market price will be impossible to predict consistently; it is a **martingale**. This is, of course, what we expect from an efficient market. I have simulated these dynamics twice below, both with an initial price $\\pi\_1(0) = 50$ ¢:

<img style="width:100%;" class='figure' src="static/doc/binary_AI09/simulated_prices.svg"/>

<details>
  <summary>Derivation of the price dynamics</summary>
  <p>
    Let $\tau := T-t$ and write  
    $$  
    \Delta(t) = \Phi^{-1}(\pi_{1}(t))\tilde{\sigma}\sqrt{\tau} - \tau\tilde{\mu}.  
    $$
    By Itô's lemma we have  
    $$  
    \mathrm{d}\pi_{1}(t) = \frac{\partial \pi_{1}}{\partial t}\mathrm{d}t + \frac{\partial \pi_{1}}{\partial \Delta} \mathrm{d}\Delta + \frac{1}{2}\frac{\partial^2\pi_{1}}{\partial \Delta^2} (\mathrm{d}\Delta)^2  
    $$  
    since $\mathrm{d}t\times\mathrm{d}\Delta = 0$. We take each term separately:  
    $$  
    (d\Delta)^2 = \tilde{\sigma}^2\mathrm{d}t  
    $$
    $$  
    \begin{align}  
    \frac{\partial \pi_{1}}{\partial t} &= \varphi\left( \frac{\Delta(t) - \tau\tilde{\mu}}{\tilde{\sigma}\sqrt{\tau}}\right) \times \frac{\partial }{\partial \tau}\left[ \frac{\Delta(t)}{\tilde{\sigma}\sqrt{\tau}} - \frac{\tilde{\mu}\sqrt{\tau}}{\tilde{\sigma}} \right] \times \frac{\partial \tau}{\partial t} \\
    &= \varphi\left( \frac{\Delta(t) - \tau\tilde{\mu}}{\tilde{\sigma}\sqrt{\tau}}\right) \times \left[ -\frac{\Delta(t)}{2\tilde{\sigma}\tau^{3/2}} - \frac{\tilde{\mu}}{2\tilde{\sigma}\sqrt{\tau}} \right] \times -1 \\ 
    &= \varphi\left( \frac{\Delta(t) - \tau\tilde{\mu}}{\tilde{\sigma}\sqrt{\tau}}\right) \times \frac{\Delta(t) + \tau\tilde{\mu}}{2\tilde{\sigma}\tau^{3/2}} \  
    \\&= \varphi(\Phi^{-1}[\pi_{1}(t)])\left[\frac{\Phi^{-1}(\pi_{1}(t))}{2\tau} + \frac{\tilde{\mu}}{\tilde{\sigma}\sqrt{\tau}}\right]  
    \end{align}  
    $$
    $$  
    \frac{\partial \pi_{1}}{\partial \Delta} = \varphi\left( \frac{\Delta(t) - \tau\tilde{\mu}}{\tilde{\sigma}\sqrt{\tau}}\right) \frac{1}{\tilde{\sigma}\sqrt{\tau}} =  
    \varphi(\Phi^{-1}[\pi_{1}(t)]) \frac{1}{\tilde{\sigma}\sqrt{\tau}}  
    $$
    $$  
    \begin{align}  
    \frac{\partial ^2\pi_{1}}{\partial \Delta^2} &= \varphi'\left( \frac{\Delta(t) - \tau\tilde{\mu}}{\tilde{\sigma}\sqrt{\tau}}\right)\frac{1}{\tilde{\sigma}^2\tau} \\  
    &= -\varphi\left( \frac{\Delta(t) - \tau\tilde{\mu}}{\tilde{\sigma}\sqrt{\tau}}\right)\frac{\Delta(t) - \tau\tilde{\mu}}{\tilde{\sigma}^3\tau^{3/2}} \\  
    &=-\varphi(\Phi^{-1}[\pi_{1}(t)]) \frac{\Phi^{-1}[\pi_{1}(t)]}{\tilde{\sigma}^2\tau}  
    \end{align}  
    $$
    Putting this together we get  
    $$  
    \mathrm{d}\pi_{1}(t) =  \frac{\varphi\left(\Phi^{-1}\left[\pi_{1}(t)\right]\right)}{\sqrt{\tau}} \mathrm{d}W_{3}(t).  
    $$
  </p>
</details>

### Evaluating Goodness-of-Fit
Starting from some assumptions about how a binary prediction market behaves, we have derived a model for the market price. How good is this model? Not great, as far as I can tell; let's dig into it! We will evaluate the model's performance only on the market for "Will Trump win the 2024 U.S. Presidential election?" shown above. This is done for brevity; the model behaves similarly on other markets.

Since the model does not allow us to forecast future prices, standard measures of prediction error will not help us evaluate the goodness of fit. We do, however, get an estimate of the instantaneous volatility, which at time $t$ it is simply
$$
\\frac{\\varphi\\left(\\Phi ^{-1}[\\pi \_1(t)]\\right)}{\\sqrt{T-t}}.
$$
Let's first compare this with the **realized volatility** of our price data. Suppose we have observed prices $\\pi\_0, \\pi\_1, \\ldots, \\pi\_n$ at times $t\_0, t\_1, \\ldots, t\_n$. Consider the straight returns
$$
r\_i := \\pi\_i - \\pi\_{i-1}, \\quad i=1, \\ldots, n.
$$
Since the price process is a martingale, the returns are zero mean (under the Archak-Ipeirotis model) and the realized volatility over each time step $[t\_{i-1}, t\_i]$ is defined as $r\_i^2$. This is a **non-parametric** but very noisy estimator of the instantaneous volatility. We will graph it alongside our model's volatility estimates. To reduce some of the noise (at the cost of slight bias) we plot a ten sample-moving average of the realized volatility below:

<img style="width:100%;" class='figure' src="static/doc/binary_AI09/volatility.svg"/>

While the model does capture the rise in volatility near market resolution, it fails to resolve any fine structure. It is also consistently higher than the realized volatility, barring some spikes. We cannot expect the Archak-Ipeirotis model to account for jumps in the price and corresponding volatility spikes, since it is driven by continuous ability processes with constant parameters. 

Next, we check how well calibrated the model is to the price data. It predicts that given the price $\\pi\_i$, the next datapoint $\\pi\_{i+1}$ has the distribution
$$
\\pi\_{i+1} \\sim \\mathcal{N}\\left(\\pi\_i, \\frac{\\varphi\\left(\\Phi ^{-1}[\\pi \_1(t\_i)]\\right)^2}{(T-t\_i)^2}(t\_{i+1}-t\_i)\\right)
$$
(We have here discretized the price dynamics using an **Euler-Maruyama scheme**.) This allows us to compute confidence interval of arbitrary confidence level. If the model correctly predicts the volatility of the data, then a 95 %-confidence interval ought to cover the true value in 95 % of cases, and so on. Below I have plotted this coverage rate against the corresponding confidence level: 

<img style="width:100%;" class='figure' src="static/doc/binary_AI09/calibration.svg"/>

Perfect model-calibration would show up as a straight diagonal in this diagram. The fact that the modeled confidence intervals consistently cover too many data points supports our previous observation that the model overestimates the true volatility. 

Finally, let's again consider to the returns $r\_i:=\\pi\_i-\\pi\_{i-1}$. Discretizing the model like before, we can derive the distribution of the returns: 
$$
r\_i \\sim \\mathcal{N}\\left(0, \\frac{\\varphi\\left(\\Phi ^{-1}[\\pi \_1(t\_i)]\\right)^2}{(T-t\_i)^2}(t\_{i+1}-t\_i)\\right).
$$
Denote its variance by $\\sigma\_i^2$. We can standardize the returns such that
$$
\\frac{r\_i}{\\sigma\_i } \\sim \\mathcal{N}(0,1).
$$
In other words, if the Archak-Ipeirotis model correctly describes the data, then these standardized returns ought to be standard normal-distributed. Below we plot their histogram (together with the standard Gaussian) and a quantile-plot.

<img style="width:100%;" class='figure' src="static/doc/binary_AI09/returns_diagnostics.svg"/>

The normalized returns are too small, compared to the standard Gaussian density, again because the model overestimates the volatilities. This also shows up in the quantile plot as non-normality in the tails, although this isn't as clear. Recall that if the data is truly standard Gaussian we expect a straight diagonal. 

At the end of the day, the Archak-Ipeirotis model does not capture the dynamics of a binary prediction market particularly well. It is poorly calibrated and systematically overestimates the price volatility. I don't think, however, that this is much of a failure. The model has zero parameters and therefore uses no historical data to tune itself. On the contrary, the fact that such a model can tell us anything at all about the price process indicates to me that Archak and Ipeirotis' basic structure is solid. They acknowledge as much themselves, when they study an **ARCH-model** of the standardized returns from their original model. The task of future statisticians is to construct more sophisticated models on top of their framework: modeling prediction market contracts as derivatives on unobservable ability processes. I think that the Archak-Ipeirotis model fails in two significant ways:
<ol>
<li>They impose unrealistic dynamics on their ability processes for the sake of deriving closed solutions. Monte Carlo techniques could allow us to estimate parameters of more sophisticated processes. For example, a mean reverting <strong>Ornstein-Uhlenbeck process</strong>, with jumps in the mean seems like a good candidate to model the incorporation of new information into the market price.</li>
<li>The price of a Archak-Ipeirotis model will always converge smoothly to either zero or one, because the market outcome is determined by which ability process is larger at the resolution time. This is not how real prediction markets behave. The U.S. 2024 presidential market prices from the beginning of the article show that by election day there is a significant amount of uncertainty left; once vote counting started the price jumped to one. This could be addressed by an alternative model of market resolution.</li>
</ol>
*Summa summarum*, good work Archak and Ipeirotis! Now it's our turn to pick up where they left off. I'm confident that a good model of prediction market volatility is within reach. 

*Published on October DD, 2025.*
