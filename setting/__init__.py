import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

from strategy import *
from .common import *

plt.rcParams["axes.grid"] = True
plt.rcParams["figure.figsize"] = (20,8)
plt.rcParams["font.family"] = "gulim"
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10.
plt.rcParams['xtick.labelsize'] = 10.
plt.rcParams['ytick.labelsize'] = 10.
plt.rcParams['axes.labelsize'] = 10.

#레이블에 '-'가 있는 경우 유니코드의 '-'문자를 그대로 출력하면 '-' 부호만 깨져 보인다. 
#이를 방지하기 위해 'axes.unicode_minus' 옵션을 False로 지정한다.
plt.rcParams['axes.unicode_minus'] = False

