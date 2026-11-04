# Forecast method

Three numbers for the period, all including deals already won in the period.

| Case | Includes | Use it for |
| --- | --- | --- |
| Worst | Won + open deals in the period at stages of 80% or more with no PAST_CLOSE, STALE or NO_NEXT_STEP flag | Cash planning and commitments. |
| Likely | Won + each open deal in the period at amount x adjusted probability | The number to manage to. |
| Best | Won + every open deal in the period that has not gone cold | Upside; what happens if everything live closes. |

Adjusted probability starts from the deal's probability (or the stage default) and multiplies:

| Condition | Multiplier |
| --- | --- |
| STALE | x 0.5 |
| PAST_CLOSE (close date in the period but already passed) | x 0.5 |
| PUSHED two or more times | x 0.7 |
| NO_NEXT_STEP | x 0.75 |

Deals whose close date passed in an earlier period are left out until the owner sets a new date; list them under "needs a new close date".

## Judgement overlays

After the numbers, add a short note when you know something the data does not:

- A deal with a verbal yes and a contract date: name it as likely to close regardless of stage.
- A deal where the champion left or budget froze: say you would remove it from likely, and why.
- Concentration: if one deal is 30% or more of the open best case, say so. The forecast depends on it.
- Seasonality: December, January and the end of the financial year in June change buying behaviour in Australia; mention it when the period crosses them.

Do not change the computed numbers to reflect overlays. Show them separately so the method stays consistent week to week.

## Coverage and movement

- Coverage = best case open pipeline / (target - won). Below 2x coverage with a month to go is a risk worth naming; below 1x means the target is out of reach without new deals.
- Show last week's three numbers beside this week's. Explain any change over 10% with the deals that caused it (won, lost, pushed in or out of the period, amount changed).

## Wording

- "Likely $54k of a $100k target, with $26k already secured in the worst case."
- Never "we will close $54k".
- Round to the nearest thousand in headlines; exact figures in tables.
