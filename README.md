
# Storage operation disaggregator

A module to disaggregate energy storage operation by time scales.
The disaggregation only requires the charging and discharging power profiles and is agnostic with respect to electricity prices or other drivers.


## Installation

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/dir/containing/storedisagg/
```

*Note: README.md created from std_example.ipynb in pre-commit hook*

## Example


```python
import sys, os
import matplotlib.pyplot as plt
import pandas as pd

import storedisagg as std

%matplotlib inline



```


```python
std.get_example_data_100()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sy</th>
      <th>echg</th>
      <th>edch</th>
      <th>mc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1.0</td>
      <td>0.123760</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2.0</td>
      <td>0.227968</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3.0</td>
      <td>0.352666</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4.0</td>
      <td>0.458185</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5.0</td>
      <td>0.499873</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>6.0</td>
      <td>0.457757</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>7.0</td>
      <td>0.351194</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>8.0</td>
      <td>0.223709</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>9.0</td>
      <td>0.112805</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>10.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>11.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>12.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>13.0</td>
      <td>0.000000</td>
      <td>0.148601</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>14.0</td>
      <td>0.000000</td>
      <td>0.212805</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>15.0</td>
      <td>0.000000</td>
      <td>0.262206</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>16</th>
      <td>16.0</td>
      <td>0.000000</td>
      <td>0.271913</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>17</th>
      <td>17.0</td>
      <td>0.000000</td>
      <td>0.219548</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>18.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>19.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>20</th>
      <td>20.0</td>
      <td>0.282191</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>21</th>
      <td>21.0</td>
      <td>0.457346</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>22</th>
      <td>22.0</td>
      <td>0.561705</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>23</th>
      <td>23.0</td>
      <td>0.563815</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>24</th>
      <td>24.0</td>
      <td>0.455124</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>25</th>
      <td>25.0</td>
      <td>0.252772</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>26</th>
      <td>26.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>27</th>
      <td>27.0</td>
      <td>0.000000</td>
      <td>0.265486</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>28</th>
      <td>28.0</td>
      <td>0.000000</td>
      <td>0.481502</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>29</th>
      <td>29.0</td>
      <td>0.000000</td>
      <td>0.617505</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>70</th>
      <td>70.0</td>
      <td>0.107125</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>71</th>
      <td>71.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>72</th>
      <td>72.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>73</th>
      <td>73.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>74</th>
      <td>74.0</td>
      <td>0.107125</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>75</th>
      <td>75.0</td>
      <td>0.800000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>76</th>
      <td>76.0</td>
      <td>0.107125</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>77</th>
      <td>77.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>78</th>
      <td>78.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>79</th>
      <td>79.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>80</th>
      <td>80.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>81</th>
      <td>81.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>82</th>
      <td>82.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>83</th>
      <td>83.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>84</th>
      <td>84.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>85</th>
      <td>85.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>86</th>
      <td>86.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>87</th>
      <td>87.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>88</th>
      <td>88.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>89</th>
      <td>89.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>90</th>
      <td>90.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>91</th>
      <td>91.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>92</th>
      <td>92.0</td>
      <td>0.000000</td>
      <td>0.107125</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>93</th>
      <td>93.0</td>
      <td>0.000000</td>
      <td>0.327341</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>94</th>
      <td>94.0</td>
      <td>0.000000</td>
      <td>0.639835</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>95</th>
      <td>95.0</td>
      <td>0.000000</td>
      <td>0.800000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>96</th>
      <td>96.0</td>
      <td>0.000000</td>
      <td>0.639835</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>97</th>
      <td>97.0</td>
      <td>0.000000</td>
      <td>0.327341</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>98</th>
      <td>98.0</td>
      <td>0.000000</td>
      <td>0.154898</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>99</th>
      <td>99.0</td>
      <td>0.000000</td>
      <td>-0.000000</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>100 rows × 4 columns</p>
</div>



## Retrieve example data
Example data with 100 time slots is generated in the storedisagg.example.example_data module.


```python
df = std.get_example_data_100()

fig, ax = plt.subplots(1, 2)

dfplot = df.set_index('sy').assign(Discharging=-df['edch'], Charging=df['echg'])
print(dfplot.head(7))

dfplot['Stored energy'] = dfplot[['Charging', 'Discharging']].sum(axis=1).cumsum()

dfplot[['Charging', 'Discharging']].plot.area(ax=ax[0])
dfplot[['Stored energy']].plot.area(ax=ax[1])
for iax, ylab in enumerate(['Power', 'Energy']): ax[iax].set_ylabel(ylab)
```

             echg  edch   mc  Discharging  Charging
    sy                                             
    0.0  0.000000  -0.0  0.0          0.0  0.000000
    1.0  0.123760  -0.0  0.0          0.0  0.123760
    2.0  0.227968  -0.0  0.0          0.0  0.227968
    3.0  0.352666  -0.0  0.0          0.0  0.352666
    4.0  0.458185  -0.0  0.0          0.0  0.458185
    5.0  0.499873  -0.0  0.0          0.0  0.499873
    6.0  0.457757  -0.0  0.0          0.0  0.457757



![png](docs/resources/README_6_1.png)


## Run disaggregation for all component profile assignment kinds

Here we loop over all component profile assignment kinds, instantiate the StDisaggregator class and call the main run() method. The printed differences shown in the output serve to compare the total profiles with the disaggregated ones and should be zero.


```python
df_full_all = pd.DataFrame()
df_step_evts_all = pd.DataFrame()

for kind in ['share', 'leftright', 'rightleft', 'top', 'bottom']:

    tvd = std.StDisaggregator(df, 1, kind)
    tvd.run()

    df_full_all = pd.concat([df_full_all, tvd.df_full], axis=0)
    df_step_evts_all = pd.concat([df_step_evts_all, tvd.df_step_evts], axis=0)

```

    100%|██████████| 6/6 [00:00<00:00, 54.77it/s]

    Difference idch (events - total): 0.0
    Difference ichg (events - total): 1.7763568394e-15
    Net value input: 0.0
    Net value disagg: 0.0
    Difference net value: 0.0


    
     67%|██████▋   | 4/6 [00:00<00:00, 35.18it/s]

    Difference idch (events - total): 0.0
    Difference ichg (events - total): 1.7763568394e-15


    100%|██████████| 6/6 [00:00<00:00, 30.10it/s]
      0%|          | 0/6 [00:00<?, ?it/s]

    Net value input: 0.0
    Net value disagg: 0.0
    Difference net value: 0.0
    Difference idch (events - total): 0.0
    Difference ichg (events - total): 1.7763568394e-15


    100%|██████████| 6/6 [00:00<00:00, 33.33it/s]
      0%|          | 0/6 [00:00<?, ?it/s]

    Net value input: 0.0
    Net value disagg: 0.0
    Difference net value: 0.0
    Difference idch (events - total): 0.0
    Difference ichg (events - total): 1.7763568394e-15


    100%|██████████| 6/6 [00:00<00:00, 45.00it/s]
      0%|          | 0/6 [00:00<?, ?it/s]

    Net value input: 0.0
    Net value disagg: 0.0
    Difference net value: 0.0
    Difference idch (events - total): 0.0
    Difference ichg (events - total): 1.7763568394e-15


    100%|██████████| 6/6 [00:00<00:00, 40.04it/s]

    Net value input: 0.0
    Net value disagg: 0.0
    Difference net value: 0.0


    


## Result dataframes

The result tables are:

### df_full_all (std.StDisaggregator.df_full)
containing the profiles of the components (nevent). It is indexed by nevents (=components) and time slot. Each nevent corresponds to a well-defined iteration.

* **echg/edch** are external charging and discharging, i.e. including losses; note that these are the original profiles, copied to each iteration
* **ichg/idch** are the temporal derivatives of the storage energy content

To obtain the external component charging and discharging profiles we need to adjust for the round trip losses.


```python
df_full_all.set_index(['kind', 'iteration', 'nevent', 'slot']).head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th>echg</th>
      <th>edch</th>
      <th>erg</th>
      <th>mc</th>
      <th>sy_orig</th>
      <th>slot_min</th>
      <th>slot_max</th>
      <th>ichg_all</th>
      <th>idch_all</th>
      <th>ichg</th>
      <th>idch</th>
    </tr>
    <tr>
      <th>kind</th>
      <th>iteration</th>
      <th>nevent</th>
      <th>slot</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="10" valign="top">share</th>
      <th>0</th>
      <th>1.0</th>
      <th>0</th>
      <td>0.000000</td>
      <td>-0.0</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0</td>
      <td>0</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <th>6.0</th>
      <th>0</th>
      <td>0.000000</td>
      <td>-0.0</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0</td>
      <td>0</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>0</th>
      <th>1.0</th>
      <th>1</th>
      <td>0.123760</td>
      <td>-0.0</td>
      <td>0.123760</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>1</td>
      <td>1</td>
      <td>0.123760</td>
      <td>0.0</td>
      <td>0.049147</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <th>6.0</th>
      <th>1</th>
      <td>0.123760</td>
      <td>-0.0</td>
      <td>0.123760</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>1</td>
      <td>1</td>
      <td>0.123760</td>
      <td>0.0</td>
      <td>0.074613</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>0</th>
      <th>1.0</th>
      <th>2</th>
      <td>0.227968</td>
      <td>-0.0</td>
      <td>0.351727</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>2</td>
      <td>2</td>
      <td>0.227968</td>
      <td>0.0</td>
      <td>0.090530</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <th>6.0</th>
      <th>2</th>
      <td>0.227968</td>
      <td>-0.0</td>
      <td>0.351727</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>2</td>
      <td>2</td>
      <td>0.227968</td>
      <td>0.0</td>
      <td>0.137438</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>0</th>
      <th>1.0</th>
      <th>3</th>
      <td>0.352666</td>
      <td>-0.0</td>
      <td>0.704394</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>3</td>
      <td>3</td>
      <td>0.352666</td>
      <td>0.0</td>
      <td>0.140050</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <th>6.0</th>
      <th>3</th>
      <td>0.352666</td>
      <td>-0.0</td>
      <td>0.704394</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>3</td>
      <td>3</td>
      <td>0.352666</td>
      <td>0.0</td>
      <td>0.212616</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>0</th>
      <th>1.0</th>
      <th>4</th>
      <td>0.458185</td>
      <td>-0.0</td>
      <td>1.162579</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>4</td>
      <td>4</td>
      <td>0.458185</td>
      <td>0.0</td>
      <td>0.181954</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <th>6.0</th>
      <th>4</th>
      <td>0.458185</td>
      <td>-0.0</td>
      <td>1.162579</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>4</td>
      <td>4</td>
      <td>0.458185</td>
      <td>0.0</td>
      <td>0.276231</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>



### df_step_evts_all (std.StDisaggregator.df_step_evts)
containing the aggregate properties of the components. This is indexed by the components (nevent). This table is generated for convenience. All properties can be generated from the df_full_all table.

Main columns:
* **ichg_final/idch_final**: Total component energy, not including losses.
* **wgt_center_erg_ichg/wgt_center_erg_idch**: Energy weighted mean of slots for charging and discharging.
* **time_diff_icd**: Time difference between charging and discharging calculated from the energy weighted means of the slots


```python
df_step_evts_all.set_index(['kind', 'iteration', 'nevent']).head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th></th>
      <th>comp_ichg</th>
      <th>comp_idch</th>
      <th>ichg</th>
      <th>idch</th>
      <th>min</th>
      <th>res_ichg</th>
      <th>res_idch</th>
      <th>slot_max</th>
      <th>slot_min</th>
      <th>wgt_center_erg_idch</th>
      <th>val_comp_idch</th>
      <th>idch_final</th>
      <th>wgt_center_erg_ichg</th>
      <th>val_comp_ichg</th>
      <th>ichg_final</th>
      <th>time_diff_icd</th>
      <th>ival_comp_net</th>
      <th>eval_comp_net</th>
      <th>eff</th>
    </tr>
    <tr>
      <th>kind</th>
      <th>iteration</th>
      <th>nevent</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="6" valign="top">share</th>
      <th rowspan="5" valign="top">0</th>
      <th>1.0</th>
      <td>1.115074</td>
      <td>1.115074</td>
      <td>2.807916</td>
      <td>1.115074</td>
      <td>1.115074</td>
      <td>1.692842</td>
      <td>0.000000</td>
      <td>19.0</td>
      <td>0.0</td>
      <td>15.180258</td>
      <td>0.0</td>
      <td>1.115074</td>
      <td>4.978642</td>
      <td>0.0</td>
      <td>1.115074</td>
      <td>10.201616</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2.0</th>
      <td>2.572953</td>
      <td>2.572953</td>
      <td>2.572953</td>
      <td>3.804610</td>
      <td>2.572953</td>
      <td>0.000000</td>
      <td>1.231657</td>
      <td>35.0</td>
      <td>20.0</td>
      <td>30.378201</td>
      <td>0.0</td>
      <td>2.572953</td>
      <td>22.470530</td>
      <td>0.0</td>
      <td>2.572953</td>
      <td>7.907670</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3.0</th>
      <td>0.813465</td>
      <td>0.813465</td>
      <td>0.813465</td>
      <td>1.274649</td>
      <td>0.813465</td>
      <td>0.000000</td>
      <td>0.461185</td>
      <td>48.0</td>
      <td>36.0</td>
      <td>41.558067</td>
      <td>0.0</td>
      <td>0.813465</td>
      <td>37.174367</td>
      <td>0.0</td>
      <td>0.813465</td>
      <td>4.383700</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4.0</th>
      <td>4.562565</td>
      <td>4.562565</td>
      <td>4.562565</td>
      <td>4.562565</td>
      <td>4.562565</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>65.0</td>
      <td>49.0</td>
      <td>60.226672</td>
      <td>0.0</td>
      <td>4.562565</td>
      <td>52.773328</td>
      <td>0.0</td>
      <td>4.562565</td>
      <td>7.453344</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5.0</th>
      <td>2.996374</td>
      <td>2.996374</td>
      <td>2.996374</td>
      <td>2.996374</td>
      <td>2.996374</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>99.0</td>
      <td>66.0</td>
      <td>95.047832</td>
      <td>0.0</td>
      <td>2.996374</td>
      <td>70.369445</td>
      <td>0.0</td>
      <td>2.996374</td>
      <td>24.678387</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <th>6.0</th>
      <td>1.692842</td>
      <td>1.692842</td>
      <td>1.692842</td>
      <td>1.692842</td>
      <td>1.692842</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>99.0</td>
      <td>0.0</td>
      <td>33.423957</td>
      <td>0.0</td>
      <td>1.692842</td>
      <td>4.978642</td>
      <td>0.0</td>
      <td>1.692842</td>
      <td>28.445314</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">leftright</th>
      <th rowspan="4" valign="top">0</th>
      <th>1.0</th>
      <td>1.115074</td>
      <td>1.115074</td>
      <td>2.807916</td>
      <td>1.115074</td>
      <td>1.115074</td>
      <td>1.692842</td>
      <td>0.000000</td>
      <td>19.0</td>
      <td>0.0</td>
      <td>15.180258</td>
      <td>0.0</td>
      <td>1.115074</td>
      <td>2.941881</td>
      <td>0.0</td>
      <td>1.115074</td>
      <td>12.238377</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2.0</th>
      <td>2.572953</td>
      <td>2.572953</td>
      <td>2.572953</td>
      <td>3.804610</td>
      <td>2.572953</td>
      <td>0.000000</td>
      <td>1.231657</td>
      <td>35.0</td>
      <td>20.0</td>
      <td>31.431444</td>
      <td>0.0</td>
      <td>2.572953</td>
      <td>22.470530</td>
      <td>0.0</td>
      <td>2.572953</td>
      <td>8.960913</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3.0</th>
      <td>0.813465</td>
      <td>0.813465</td>
      <td>0.813465</td>
      <td>1.274649</td>
      <td>0.813465</td>
      <td>0.000000</td>
      <td>0.461185</td>
      <td>48.0</td>
      <td>36.0</td>
      <td>42.184759</td>
      <td>0.0</td>
      <td>0.813465</td>
      <td>37.174367</td>
      <td>0.0</td>
      <td>0.813465</td>
      <td>5.010392</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4.0</th>
      <td>4.562565</td>
      <td>4.562565</td>
      <td>4.562565</td>
      <td>4.562565</td>
      <td>4.562565</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>65.0</td>
      <td>49.0</td>
      <td>60.226672</td>
      <td>0.0</td>
      <td>4.562565</td>
      <td>52.773328</td>
      <td>0.0</td>
      <td>4.562565</td>
      <td>7.453344</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



## Illustration of disaggregation

### Plot of components for all profile assignments.


```python
# Add efficiencies to compensate for round trip losses
dfplot = df_full_all.join(df_step_evts_all.set_index(['nevent', 'kind'])['eff'], on=['nevent', 'kind'])

dfplot = dfplot.assign(Charging=dfplot.ichg / dfplot.eff, Discharging=-dfplot.idch * dfplot.eff)
dfplot = dfplot.set_index(['kind', 'nevent', 'slot'])
dfplot['Stored energy'] = dfplot.groupby(level=['kind', 'nevent']).apply(lambda x: (x.Charging + x.Discharging).cumsum().reset_index([0, 1], drop=True))
dfplot = dfplot.sort_index()
dfplot.loc[dfplot['Stored energy'].abs() < 1e-4, 'Stored energy'] = 0

dfplot = dfplot.pivot_table(index=['kind', 'slot'], columns=['iteration', 'nevent'], values=['Charging', 'Discharging', 'Stored energy'])

fig, axarr = plt.subplots(5, 2, sharex=True)
fig.set_size_inches(10, 8)
map_ax = [(0, ['Charging', 'Discharging'], 'Power'),
          (1, ['Stored energy'], 'Energy')]

for ax_x, cols, ylabel in map_ax:
    for ax_y, kind in enumerate(dfplot.index.get_level_values('kind').unique()):

        ax = axarr[ax_y, ax_x]
        dfplot.loc[kind][cols].plot.area(linewidth=0, ax=ax, stacked=True, legend=False)
        ax.set_ylabel(ylabel)
        ax.set_title(kind)
```


![png](docs/resources/README_14_0.png)


### Plots by iteration for all profile assignments.


```python
dfplot = dfplot.sum(level=[0, 'iteration'], axis=1)
fig, axarr = plt.subplots(5, 2, sharex=True)
fig.set_size_inches(10, 8)
map_ax = [(0, ['Charging', 'Discharging'], 'Power'),
          (1, ['Stored energy'], 'Energy')]

for ax_x, cols, ylabel in map_ax:
    for ax_y, kind in enumerate(dfplot.index.get_level_values('kind').unique()):

        ax = axarr[ax_y, ax_x]
        dfplot.loc[kind][cols].plot.area(linewidth=0, ax=ax, stacked=True, legend=False)
        ax.set_ylabel(ylabel)
        ax.set_title(kind)
```


![png](docs/resources/README_16_0.png)

