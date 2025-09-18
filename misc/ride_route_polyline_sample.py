'''
# 必要ライブラリのインポート
- polyline：エンコード済み文字列を緯度経度に変換
- requests：API呼び出しに使う
- matplotlib：描画とアニメーション
- geopy.distance：２点間の距離計算
- contextily / geopandas / shapely：背景地図と地理情報の扱い
- pyproj：座標系の変換
'''
import time
import polyline
import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from geopy.distance import geodesic
from datetime import datetime
import contextily as ctx
import geopandas as gpd
from shapely.geometry import LineString
from matplotlib.animation import FFMpegWriter
from pyproj import Transformer
from itertools import islice
from scipy.signal import savgol_filter, medfilt

'''
# 入力データの準備
- encoded_polyline に走行ルートのエンコード済みポリライン文字列を指定
  - これは Google が定義する Encoded Polyline Algorithm Format （通称：Google のエンコード済みポリライン形式）です。
  - Strava や Google Maps API、Leaflet など多くの地図サービスで使われている 緯度・経度の連続を短い文字列に圧縮するアルゴリズムです。
  - Python では polyline ライブラリでこの形式のデコードとエンコードができます。
- start_time／end_time で走行開始・終了の時刻を指定
'''
encoded_polyline = "chswEcyarYtBdFhEtKf@|B`AjFfB~IZjBLbB`@rNH`BALDbBp@~S?JCJ@r@XzHFdDJ|BFnCUjKW|PIdCQ|B[vCmB~OuAbMMzAEhCJzKNtKHx@v@hEl@lCRfAv@nDLb@VXNBp@APBl@b@RDjA@PB`@XZb@Rh@@j@E~@?TBPFPLJLJp@V`@VXj@HTz@lCHd@@\\A^g@bGCbAHl@h@lANj@f@bC?`@GhAE`BLbECj@UbC?h@Hd@Vj@BPPlAT~BCNGJ{@^CHARP`FbA|RRzEBbBA`EIpLBl@StUA`C\\z`@HfGAbAZzIBdBExAWtDEtASvBMr@C\\C`B@p@dAzNNpAHNHd@HdAv@dEfBdGj@`B`A|B|A`D~B|Dp@nA`AnBf@tAX\\BLARU`@mCnDu@hAeAlBBDH?bAaBTOhCa@N@HL`@xDB`@?\\Kt@_@zA]rBKRYPIN?JBPNXFVD\\A|BKjFZfHJpA~A`JVx@x@jBTt@Hv@J`EBP`@@jBKtBCvFJfC@j@F|CbA|@NlDXpEd@zAFv@E`@GvF_Bz@Sz@If@@f@Db@Jh@Pf@XrBtApAf@\\Dt@V|A`@nBb@bAb@h@Zn@r@tAjCTVbBx@`EbBH@EHOFJ\\GJSVwAlAg@j@wAvBM\\Ax@Bl@AfAAtDCv@o@rC]xBk@lCWvAc@vF_ArH[xAq@rBkApEc@fD{AbGkBzKMhBEhGAxBFjD?dBHhBXlBFx@IfAu@|CMt@QzBIpEGxAIz@q@tF]bBMVIHKDYDY@gEEe@@WB_@R_AlAg@\\a@NsATWJYVS`@y@rEW`BKZSVOJQF}BHk@Li@T{DpBm@TyA^[Nm@`@sCjCkBbCuBxBg@r@m@nAUZk@^oAd@q@\\_@VsC|BSZQf@[xBAv@F^Nf@JPp@n@~@r@l@p@l@vAZhAJrBIpC@|@I~CAzA?r@Dp@L\\Vb@t@r@nB|Al@Pl@Dz@@RBRAPBZL`@ZfAvAx@`Af@b@|@p@fAh@l@RZR`A^ZHVBTATE`@QRO~@oAb@]j@QbB[f@OdAi@nBqAfAWd@Q`AKr@FdB\\`@PRNL\\BR@`@c@fD_@~BEf@AZDh@lAdJHbACv@G`@M`@k@xAI\\C`@@n@XfCBf@A`AN|AAt@Ij@g@|A]`AY^ULODsAJqATaA\\[Nm@`@{A|Ak@f@m@`@{@`@k@\\]ZSVQVo@tAc@t@wCbE[V[PUDuAL]FWJ]TMR]p@o@x@Sf@M`@QXk@l@_Ap@{@x@ORMX[b@m@d@e@h@o@~@s@b@kA\\cA~@QVo@dB[l@m@z@i@n@]l@iArCs@vAi@bBMPMNULMDgAj@i@`@w@jAm@lAQF_@Ao@Dc@Cc@Bs@\\aAr@WBm@KW?{@Xw@x@[NKBcAAWDYHc@Xu@z@[PqCh@SNMPY|@QBg@Ei@@m@Lu@V}@b@uA`AmAfA{ApAy@lAUd@SlAKzACTK`@QXg@ZwBj@g@PUPSRILQd@KJc@T_BXKDYTOXGXCj@@rAGt@GXQ`@STo@t@g@f@m@X[Vg@v@c@Va@J[NkA|ASN_@PURcApAKRC\\D`@@VG\\OTQLo@LUJWZ?BOPa@x@SZcAj@m@XMNSd@IN]Na@J{AjA]^GLET@VFLRTt@PVNLVBR?RI\\MPSLYB_@Mg@YOCQBOJg@x@SR{@To@FsAZa@LqBz@u@f@wBtBo@h@{@h@gBv@o@d@[\\Wb@wH`Pi@~@c@d@cAv@cGhEa@^UVc@z@Sr@e@bCOb@[j@wGfJgFtFiAdA[Rm@P}AJi@Ha@RWVWd@K^s@|CSl@Ul@_@d@c@\\c@TcD`AeA`@c@HW@qB@i@Ha@J}B|@{B~@gA^g@L{BzBGl@ML}@b@Ul@O@LGBMGr@O^OXw@fA}KtNAJ@TDVzEtOx@hCRf@Zd@X^h@`@^PH@DEHy@AhAKnA?f@@LRLFHBCACUKSBOIC@?FT?BCBwBEIq@_@a@YY[g@_Ay@cC}EqOW_AAWHUvJgMpCyDNg@LiAd@_CRc@x@QTKJGHOJGL?FDZDf@@l@KjAa@zCkAh@Mh@G`B?h@GZGr@]x@Y`Ai@j@QZQ`Ay@RYd@gAv@{CL[Ze@TSb@UXGjBMf@Mf@Wb@_@|@cAz@w@zAaB`AkAdF_Hj@}@Zq@Lc@h@sCZs@Ta@b@g@t@o@dGgEv@u@RWjCoF`EoIZk@^g@ZWZSzAs@r@c@TOhCeC~@s@x@a@tAi@lDu@^MNKJQTe@LOLKRER@t@b@PDP?PGJMDS?WGSMQs@SQKMMGSAU@WHSLO|AaBNI^ENENKRe@JSNM`By@NQh@eA^g@POPIf@KPILOHS@UCo@BYTm@NSt@y@~@q@b@m@f@i@RKj@STMPQ^i@RQ`Ao@j@e@f@i@NYL]F_@Da@A_BB_@H[N[RSVM~Ac@TMPU\\o@PUTQn@UtBo@RMPSLUHYT}BVaA~@_B\\a@nD{Cv@m@z@g@vAe@n@EV?VFh@RfAn@^NLD^Dh@?~De@h@Ij@O|@a@lCkBn@i@r@u@lC}CR[jAgCp@aAj@e@^Qv@YPKLMJSd@sA~@oBpA}C`BaClAqCR]^c@b@a@ZMfAUVQlAaBr@o@|@yAvCkCNUTq@Vk@l@w@j@}@POj@UVGxAOj@OPK`@c@tBqC~@}Ap@yA`@i@n@o@rAo@r@g@p@m@`AeAj@c@p@_@f@OzB]h@Q\\G\\SJKPa@~@eCHw@Aa@MgA@qACq@YoC?m@BWJi@r@gBJo@BYAu@uA_KEs@Ds@n@{DPaB?o@CUGSKM[SgCy@]C[@aARm@RqC`Bm@Xm@PoB`@]Ni@\\}@jA_@Xu@Tc@Be@GmAc@yB_Aw@c@kAeAyBkCa@WKE[CeBL]?[Ee@Su@s@eBiB]i@Oa@Ge@?_BTyJAw@M_Au@qBaAkBg@o@gAoAS_@Mc@Gg@B{@LmAP{@Pe@Va@bCqBd@[d@UfBu@\\SR[l@mAf@u@lBmBbB}B`@c@|@}@dA}@l@a@p@[tBm@tDqB|@a@l@IdBCLCZQHKN]rAqHPg@NO`@UpAUf@Od@[hAuA^Sb@E`FF\\AZKPUDMVeAN{@\\mCPcBH_B@{@Cs@BkAHuAPsA~@eEJ{@E}@UeBKoAIeI@cDDqEDiAHw@f@aDbAqFxAyFZgCLs@jAsEl@kBR{@L}@x@oG\\{EFg@vAuHn@wCD_A?gI@]F[Vi@hAcB`@g@v@s@t@w@FKDMCMIIYIwFgC]a@s@yAa@s@m@m@m@_@_@Qk@QkDq@wA_@eAe@}AgAkAs@e@Se@K{@Ig@?c@Bs@LiGfBi@Hy@BaCMoFc@gCW}@UsBs@u@KeEK}CEoCDyBNCAAMICEGMyDGk@Mg@cAcC[aA_BgJKaAYqGAgBLcHAW]_AAUBQJMNILOn@cDNiABc@Cu@[_EEGK?sCd@SPy@vAGBGI@Cz@yA~@wA`C}CHEMWKg@kAuCgAyBqDkGwA{CkA_Dw@{Bs@sC]_BcAyFM_@YkAOGAKLg@@o@WqF?c@KoC?g@LeCP{BDW`@mDHaADeA@q@]sLIm@Ae@?{D[{`@?kEH_IVu\\M}IqAgXWaDBKBClA_@DC@E]uDIi@]{@Ge@Bo@TuC?g@MqD@a@H}ABy@c@gCOe@g@iAKa@Cc@TwD?SGURe@HyA?OQaAaAyCa@a@mAs@KKIOGe@@sBQk@S[QMUI]Ec@@g@GQIU[KG[Ci@DSCOIIKISS}@cDaQO{AEaBAuCKgFCyCAkDDaBLcBjBkPZsC@_@lA{JPgBJ_CFqD^}Q@{HIuDQkHSeEK}CGeAO_JUcHa@cPMoBSuAkAmGaA{EQcAu@cDU{@MWIGK[W}@u@qB[}@GGI?KD{BpAeBjAsD`CyJxG_Al@QFGAIKSm@k@eAi@qB[k@DK"
start_time = datetime.strptime("2023-01-01 08:00:00", "%Y-%m-%d %H:%M:%S")
end_time = datetime.strptime("2023-01-01 9:30:00", "%Y-%m-%d %H:%M:%S")

'''
# ルートのデコードと距離・速度の算出
'''
# ルート(polyline)のデコード
points = polyline.decode(encoded_polyline)  # [(緯度,経度)]

# 各点間の累積距離を計算
distances = [0.0]
for i in range(1, len(points)):
    d = geodesic(points[i-1], points[i]).meters
    distances.append(distances[-1] + d)

'''
# 標高データの取得（間引き＋API呼び出し）    
- sample_points()：50m間隔で座標を間引き
- get_elevations()：APIへ一括リクエストして標高を取得
- Open-Elevation: 無料で使えるがレート制限あり。
'''
def sample_points(points, interval_m=50):
    sampled = [points[0]]
    last = points[0]
    for p in points[1:]:
        if geodesic(last, p).meters >= interval_m:
            sampled.append(p)
            last = p
    return sampled

def get_elevations(coords):
    url = "https://api.open-elevation.com/api/v1/lookup"
    locations = [{"latitude": lat, "longitude": lon} for lat, lon in coords]
    response = requests.post(url, json={"locations": locations})
    data = response.json()
    # {'results': [{'elevation': 81.0, 'longitude': 139.43735, 'latitude': 35.50113}, {'latitude': 35.50119, 'longitude': 139.43668, 'elevation': 81.0},...]}
    return [loc["elevation"] for loc in data["results"]]

def chunked(iterable, size):
    it = iter(iterable)
    while True:
        chunk = list(islice(it, size))
        if not chunk:       # 空リストならもう要素がない
            break
        yield chunk

sampled_points = sample_points(points)
chunks = list(chunked(sampled_points, 100))  # 100点ずつ
elevations = []
for c in chunks:
    elevations += get_elevations(c)
    time.sleep(1.2)  # 秒間リクエスト数を1以下に抑える

# 標高データの平滑化
# ＊Savitzky–Golay フィルタで滑らかに（小さなノイズを除去、形状を保持）
# elev_sg = savgol_filter(elevations, window_length=11, polyorder=2)
# ＊メディアンフィルタでスパイク除去（より荒いトゲ取りに有効）    
elev_med = medfilt(elevations, kernel_size=9)
elevations = elev_med

'''
ルート線ジオメトリを作成
GeoDataFrame の作成
geometry=[line] で LineString（ルートの線）を要素に持つ
crs="EPSG:4326" でその線が「WGS84（緯度経度）」座標系で定義されていることを指定
座標系の変換
.to_crs(epsg=3857) によって「Web Mercator（メートル単位の地図投影）」に再投影
WGS84（4326）は曲面上の角度（°）緯度・経度で地球上の位置を表す座標系。GPS もこの形式を使う。
Web Mercator（3857）は平面上の長さ（m）地図タイルサービス（OpenStreetMap や Google Maps）で広く使われる投影。

'''
line = LineString([(lon, lat) for lat, lon in points])
gdf = gpd.GeoDataFrame(geometry=[line], crs="EPSG:4326").to_crs(epsg=3857)
bounds = gdf.total_bounds # [xmin, ymin, xmax, ymax]

'''
figsize=(12, 9) は図全体の「幅」を 12 インチ、「高さ」を 9 インチに設定します。 この物理サイズと、fig.set_dpi() で指定した DPI から最終的なピクセル解像度が決まります。
幅（px） = 幅（inch） × DPI
高さ（px） = 高さ（inch） × DPI
たとえば DPI=150 の場合、幅は 12 × 150 = 1800px、 高さは 9 × 150 = 1350px になります。
'''
fig, (ax_map, ax_elev) = plt.subplots(
    2, 1,
    figsize=(12, 9),
    gridspec_kw={'height_ratios': [10, 2]}  # 地図5：標高1 の比率
)
fig.set_dpi(150)

# ルート線の描画
gdf.plot(ax=ax_map, linewidth=2, color='blue')

x_margin = (bounds[2] - bounds[0]) * 0.1  # 横幅の10%をマージン
y_margin = (bounds[3] - bounds[1]) * 0.1  # 高さの10%をマージン
ax_map.set_xlim(bounds[0] - x_margin, bounds[2] + x_margin)
ax_map.set_ylim(bounds[1] - y_margin, bounds[3] + y_margin)
ax_map.tick_params(
    left=False,      # 左側のティックマークを消す
    bottom=False,    # 下側のティックマークを消す
    labelleft=False, # 左側のラベルを消す
    labelbottom=False# 下側のラベルを消す
)

# zoom レベルを上げるとタイルの解像度が細かくなる
# Mercator 投影済みの ax_map に標準 OSM（Mapnik）タイルを背景に貼る
'''
contextily とは
contextily は Python で Web 上の地図タイル（背景地図）を取得し、matplotlib の図や GeoTIFF などに手軽に貼り付けられる小規模パッケージです。地理空間データを扱う他のライブラリ（GeoPandas や Rasterio）ともシームレスに連携できます。
'''
ctx.add_basemap(
    ax_map,
    source=ctx.providers.OpenStreetMap.Mapnik,
    zoom=14   #  例: 12→広域、14→詳細
)
marker, = ax_map.plot([], [], 'ro')

# 標高グラフ描画
sampled_distances = [0.0]
for i in range(1, len(sampled_points)):
    d = geodesic(sampled_points[i-1], sampled_points[i]).meters
    sampled_distances.append(sampled_distances[-1] + d)

ax_elev.plot(sampled_distances, elevations, color='gray')
elev_cursor = ax_elev.axvline(x=0, color='red')
ax_map.set_title("ride route")
# 標高グラフタイトル・軸ラベル
ax_elev.set_title("elevation", fontsize=10)
ax_elev.tick_params(axis='both', labelsize=8)

# マージン調整で上下の隙間を削減
#plt.subplots_adjust(hspace=0.1)

# アニメーション更新関数
# 緯度経度→Web Mercator 変換
transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
merc_x, merc_y = zip(
    *[transformer.transform(lon, lat) for lat, lon in points]
)

def update(frame):
    x = merc_x[frame]
    y = merc_y[frame]
    marker.set_data([x], [y]) # 現在位置マーカーを更新
    d = distances[frame]
    elev_cursor.set_xdata([d, d]) # 標高グラフカーソルを更新
    return marker, elev_cursor

'''
# アニメーションの作成と保存
update 関数の戻り値 更新した Line2D や Patch オブジェクトを必ず返す必要があります。
地図や固定テキストなど、動かない要素は最初に描画を済ませておきます。
blit=True を指定すると、更新が必要な部分だけを再描画する仕組み（blitting）を有効化します。これにより、毎フレームで全体を再描画するのではなく、変更されたアーティスト（点や線など）だけを高速に差分更新するので、アニメーションがスムーズになります。
'''
fps = 10
ani = animation.FuncAnimation(fig, update, frames=len(points), interval=int(1000/fps), blit=True)

writer = FFMpegWriter(fps=fps, codec="h264", metadata={}, bitrate=3000)
ani.save("run_animation.mp4", writer=writer, dpi=100)
