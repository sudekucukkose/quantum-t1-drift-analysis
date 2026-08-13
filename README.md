# Quantum T1 Drift Analysis

Kuantum bilgisayar donanımlarında qubit performansının zaman içinde nasıl değişebileceğini incelemek amacıyla geliştirilmiş bir istatistiksel analiz projesidir.

Bu projede özellikle **T1 relaxation time** metriğine odaklanılmıştır.

## Proje Hakkında

Kuantum donanımlarında qubit özellikleri zaman içinde değişebilir. Kalibrasyonlar, çevresel koşullar ve farklı kaynaklardan gelen değişkenlikler bu değerlerde dalgalanmalara neden olabilir.

Bu çalışmada Qiskit'in `FakeBrisbane` backend'i başlangıç noktası olarak kullanılmıştır. Backend'den alınan T1 değerleri kullanılarak 20 zaman adımından oluşan sentetik bir zaman serisi oluşturulmuştur.

Sentetik veriye küçük rastgele değişimler eklenmiş ve qubitlere farklı drift oranları verilerek farklı davranış örnekleri oluşturulmuştur.

> **Not:** Bu projede kullanılan zaman serisi sentetiktir. Gerçek bir IBM Quantum işlemcisinden sürekli olarak toplanmış ölçümleri temsil etmez.

## Araştırma Sorusu

Basit istatistiksel ve zaman serisi yöntemleri kullanılarak qubitlerin T1 performansındaki zamansal değişimler nasıl izlenebilir?

Çalışmada özellikle şu sorular ele alınmaktadır:

- T1 değeri zaman içinde nasıl değişiyor?
- Qubitler benzer bir davranış mı gösteriyor?
- Başlangıç ve bitiş değerleri arasındaki değişim ne kadar?
- Hangi qubitlerde negatif bir trend görülüyor?
- Basit istatistiksel göstergeler olası drift davranışlarını işaret edebilir mi?

## Yöntem

Analiz genel olarak şu şekilde ilerlemektedir:

FakeBrisbane
↓
Başlangıç T1 değerleri
↓
Sentetik zaman serisi
↓
Qubit bazlı analiz
↓
Trend analizi
↓
Drift sınıflandırması
↓
Grafikler ve rapor

### 1. FakeBrisbane

Qiskit'in fake backend altyapısındaki `FakeBrisbane` kullanılmıştır.

İlk olarak seçilen qubitlerin mevcut T1 değerleri alınmış ve sentetik veri üretiminde başlangıç değeri olarak kullanılmıştır.

### 2. Sentetik Veri

Her qubit için 20 zaman adımı oluşturulmuştur.

Veriye küçük rastgele değişimler eklenerek ölçüm benzeri dalgalanmalar simüle edilmiştir. Ayrıca qubitlere farklı drift oranları verilmiştir.

Bu sayede:

- kararlı davranış,
- hafif negatif drift,
- daha belirgin negatif drift,
- hafif pozitif değişim

gibi farklı senaryolar oluşturulmuştur.

Bu değerler deneysel olarak oluşturulmuştur ve gerçek donanım ölçümleri değildir.

### 3. Trend Analizi

Her qubit için aşağıdaki değerler hesaplanmıştır:

- Mean T1
- Start T1
- End T1
- Percentage change
- Trend slope
- R²
- Status

T1 değerlerinin zaman içindeki yönünü görmek için basit bir linear regression modeli kullanılmıştır.

**Trend slope**, T1 değerinin artma veya azalma yönünü gösterir.

**R²**, doğrusal modelin gözlenen veriyi ne ölçüde açıkladığını gösteren bir uyum ölçüsüdür.

### 4. Drift Sınıflandırması

Qubitler başlangıç-bitiş arasındaki yüzde değişime göre üç gruba ayrılmıştır:

| Status | Açıklama |
|---|---|
| STABLE | Görece kararlı davranış |
| WATCH | Hafif negatif değişim |
| DEGRADING | Daha belirgin negatif değişim |

Bu eşikler yalnızca bu proje için tanımlanmıştır. IBM tarafından belirlenmiş resmi donanım limitleri değildir.

## Görselleştirmeler

### Average T1 Temporal Trend

Seçilen qubitlerin ortalama T1 değerinin zaman içindeki değişimini gösterir.

### Qubit-Level T1 Trends

Her qubitin T1 davranışını ayrı ayrı gösterir. Böylece tek bir ortalama değerin arkasında kalan qubit bazlı farklılıklar görülebilir.

### T1 Heatmap

Qubitleri ve zaman adımlarını aynı grafik üzerinde göstererek genel değişimi görmeyi kolaylaştırır.

## Çıktılar

Program çalıştırıldığında `outputs/` klasörü altında şu dosyalar oluşturulur:

outputs/
├── synthetic_t1_timeseries.csv
├── qubit_trend_report.csv
├── overall_t1_trend.png
├── qubit_t1_trends.png
└── t1_heatmap.png

`synthetic_t1_timeseries.csv` oluşturulan zaman serisini içerir.

`qubit_trend_report.csv` ise her qubit için hesaplanan trend istatistiklerini içerir.

## Kullanılan Teknolojiler

- Python
- Qiskit
- Qiskit IBM Runtime
- NumPy
- Pandas
- Matplotlib
- Linear Regression
- Time-Series Analysis

## Kurulum

Gerekli paketleri yüklemek için:

pip install -r requirements.txt

Programı çalıştırmak için:

python main.py

## Tekrarlanabilirlik

Sentetik veri üretiminde sabit bir random seed kullanılmıştır:

RANDOM_SEED = 42

Bu sayede aynı kod ve ortam kullanıldığında aynı sentetik veri setinin yeniden oluşturulması hedeflenmiştir.

## Sınırlamalar

Bu çalışma gerçek zamanlı quantum hardware monitoring sistemi değildir.

Kullanılan zaman serisi sentetiktir ve `FakeBrisbane` değerleri yalnızca başlangıç noktası olarak kullanılmıştır. Bu nedenle elde edilen trendler gerçek bir IBM Quantum cihazında fiziksel bir bozulmanın kanıtı olarak yorumlanmamalıdır.

Ayrıca çalışma yalnızca T1 metriğine ve 20 simüle edilmiş zaman adımına odaklanmaktadır.

Amaç, gerçek donanım verilerine geçmeden önce kullanılabilecek basit bir analiz yaklaşımını göstermektir.

## Gelecek Çalışmalar

Projeyi geliştirmek için birkaç farklı yön düşünülebilir:

- T2 coherence analizi
- Readout error analizi
- Gate error analizi
- Confidence interval hesaplamaları
- Statistical significance testing
- Change-point detection
- Anomaly detection
- Gerçek quantum hardware calibration verilerinin kullanılması

Daha ileri bir aşamada bu metrikler birleştirilerek **Quantum Hardware Health Score** gibi daha kapsamlı bir monitoring yaklaşımı geliştirilebilir.

## Sonuç

Bu proje, qubitlerin T1 relaxation time değerlerini sentetik bir zaman serisi üzerinden inceleyen küçük bir prototiptir.

Buradaki amaç bir kuantum işlemcisinin fiziksel ömrünü tahmin etmek değildir.

Daha çok, qubit seviyesinde zaman içinde ortaya çıkabilecek değişimleri ve olası drift davranışlarını basit istatistiksel yöntemlerle izleyebilmek için bir başlangıç noktası oluşturmaktır.

## Author

**Quantum Computing × Statistics × Data Science**

Kuantum hesaplama, istatistik ve veri biliminin kesişiminde kişisel bir portföy çalışması.
