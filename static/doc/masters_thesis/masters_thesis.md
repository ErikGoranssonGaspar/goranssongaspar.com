## Final Words on Timing Prediction Markets
I've spent the last year thinking about how to model prediction market prices. Although there has been a lot of work done on these markets in general, the pricing problem is not particularly well studied. It's only recently, with the advent of large platforms like Polymarket and Kalshi, which host many highly liquid markets on a wide range of topics, that it has made sense to treat prediction market contracts like any other financial derivative and price them using standard methods from mathematical finance.

<a target="_blank" href="/binary-AI09">My first article</a> covered one of the best existing models, published by <a target="_blank" href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1268442">Archak and Ipeirotis (2009)</a>, for binary election-style markets. At some point, however, I recognized that a large number of markets, particularly those on geopolitical topics, aren't particularly compatible with this style of model.

What I call **timing markets** are based on questions like, "Will event A happen before time T?" Unlike election-style markets, timing market prices go to zero as the deadline approaches, because there is simply less time left for event A to occur, all else being equal. I first presented this idea <a target="_blank" href="/OU-timing">in a previous post</a>. When you've made the distinction between election-style markets and timing markets, it is natural to construct a model of the latter by supposing that underlying event A arrives with an inhomogeneous Poisson process. The market price then becomes the process' conditional survival probability past the deadline $T$, and the key modeling decision is the dynamics of the corresponding intensity process. This turns out to give a pricing equation that is equivalent to the one used for reduced-form models of defaultable corporate bonds and, more significantly, zero-coupon bonds with a stochastic short rate. I'm quite happy with this analogy which, as far as I can tell, did not previously exist in the literature. It allows us to leverage the very powerful tools developed for conventional bond pricing to model timing prediction markets.

My master's thesis, which I recently defended, became an elaboration of the ideas first explored in that blog post. Instead of an Ornstein-Uhlenbeck intensity, which is analytically easier to work with but is not strictly non-negative, I considered an intensity process with mean-reverting Cox-Ingersoll-Ross dynamics, with jumps modelling news shocks. I also do more rigorous validation on four different timing markets. These markets are quite efficient, so price forecasting is unsurprisingly difficult, but I'm able to demonstrate reasonably good calibration across the entire predictive distribution. This suggests that these models could be useful in risk management and market-making applications. Parameters are estimated using a Kalman-filter-based quasi-maximum likelihood technique, which makes it easy to fit the model to multiple timing markets based on the same event but with different deadlines. There are interesting questions left to answer about how consistently these markets are priced; inefficiencies would present an arbitrage opportunity.

I will refrain from posting a thorough write-up of my work here. A more elaborate summary is given on the poster below, which I will present at the Young Statisticians Meeting set to be held in Cambridge this year:

<iframe src="static/doc/masters-poster.pdf" style="width:100%; height:800px; border: solid var(--text-color) var(--line-width); border-radius: var(--border-radius); margin-bottom: 1em; max-width: 100%; overflow: hidden;"></iframe>

For the interested reader, here is the text of my full thesis:

<iframe src="static/doc/masters-thesis.pdf" style="width:100%; height:800px; border: solid var(--text-color) var(--line-width); border-radius: var(--border-radius); margin-bottom: 1em; max-width: 100%; overflow: hidden;"></iframe>

In the name of completeness, you can also find the slideshow used for my thesis defense here:

<iframe src="static/doc/masters-presentation.pdf" style="width:100%; height:800px; border: solid var(--text-color) var(--line-width); border-radius: var(--border-radius); margin-bottom: 1em; max-width: 100%; overflow: hidden;"></iframe>

*Published in July 2026.*
