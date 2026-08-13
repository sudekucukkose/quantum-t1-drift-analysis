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

## Bulgular ve Yorum

Sentetik zaman serisi üzerinde yapılan analiz, qubitlerin zaman içindeki T1 davranışlarının tamamen aynı olmadığını göstermektedir. Bazı qubitlerde negatif değişim görülürken, bazıları daha kararlı bir davranış göstermiştir.

### Qubit Bazlı Bulgular

QUBİT	   T1 DEĞİŞİMİ	  TREND SLOPE  R^2	    STATUS
QUBİT 0	  -0.80%       	NEGATİF   	 0.376	  WATCH
QUBİT 1	 -2.58%	        NEGATİF   	 0.574  	DEGRADING
QUBİT 2	 -3.26%	        NEGATİF	     0.882	  DEGRADING
QUBİT 3   +0.10%       	POZİTİF    	 0.170	  STABLE
QUBİT 4	 -1.09%	        NEGATİF	     0.533  	DEGRADING

**Qubit 0:** T1 değeri yaklaşık %0.80 azalmıştır. Trend slope negatif olsa da R² değeri 0.376'dır. Bu nedenle değişim yönü aşağı olsa da doğrusal trend çok güçlü değildir. Qubit 0 WATCH olarak sınıflandırılmıştır.

**Qubit 1:** T1 değeri yaklaşık %2.58 azalmıştır. Negatif trend slope ve 0.574 R² değeri, zaman içinde aşağı yönlü bir değişim olduğunu göstermektedir. Qubit 1 DEGRADING olarak sınıflandırılmıştır.

**Qubit 2:** En belirgin negatif değişim Qubit 2'de görülmektedir. T1 değeri yaklaşık %3.26 azalmış ve trend slope negatif çıkmıştır. R² değerinin 0.882 olması, oluşturulan sentetik veride doğrusal negatif trendin diğer qubitlere göre daha belirgin olduğunu göstermektedir. Bu nedenle Qubit 2 DEGRADING olarak sınıflandırılmıştır.

**Qubit 3:** T1 değeri yaklaşık %0.10 artmıştır. Trend slope pozitiftir ancak R² değeri 0.170 olduğu için güçlü bir doğrusal trend bulunduğu söylenemez. Projede kullanılan eşiklere göre Qubit 3 STABLE olarak sınıflandırılmıştır.

**Qubit 4:** T1 değeri yaklaşık %1.09 azalmıştır. Negatif trend slope ve 0.533 R² değeri, aşağı yönlü bir değişim olduğunu göstermektedir. Qubit 4 DEGRADING olarak sınıflandırılmıştır.

### Genel Değerlendirme

Beş qubitin üçü DEGRADING, biri WATCH ve biri STABLE olarak sınıflandırılmıştır.

Genel ortalama T1 grafiği, T1 değerlerinin zaman boyunca küçük dalgalanmalar gösterdiğini ve serinin son bölümünde daha düşük seviyelere ulaştığını göstermektedir.

Qubit bazlı trend grafiği, qubitlerin farklı başlangıç T1 seviyelerine sahip olduğunu ve zaman içinde farklı yönlerde değişebildiğini göstermektedir. Heatmap de bu seviye farklarını ve zaman içerisindeki değişimleri birlikte görmeyi sağlamaktadır.

Grafiklerdeki değişimler genel olarak küçük görünse de CSV sonuçları değişimlerin yönünü daha net ortaya koymaktadır. Özellikle Qubit 2'nin %3.26'lık değişimi, negatif trend slope değeri ve 0.882 R² değeri, sentetik veri setinde en belirgin negatif trendin bu qubitte olduğunu göstermektedir.

Bu sonuçlar, yalnızca grafiklere bakmak yerine yüzde değişim, trend slope ve R² gibi basit istatistiksel göstergelerin birlikte değerlendirilmesinin zamansal değişimleri incelemek açısından faydalı olabileceğini göstermektedir.

Ancak bu sınıflandırmalar yalnızca proje kapsamında oluşturulan sentetik veri ve eşikler üzerinden yapılmıştır. DEGRADING olarak sınıflandırılan bir qubitin gerçek bir quantum processor üzerinde fiziksel olarak bozulduğu sonucuna varılamaz.

Bu çalışmanın temel amacı, gerçek donanım verilerine geçmeden önce T1 gibi bir donanım metriğinin zaman içerisindeki değişimini takip etmek için kullanılabilecek basit bir analiz yaklaşımını göstermektir.

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
