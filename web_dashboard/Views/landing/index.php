<?php
/**
 * File:	/nao-smart-ai/web_dashboard/Views/landing/index.php
 * @package NAO-Smart-AI
 * @author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
 *
 * Created Date: Tuesday, December 17th 2025, 10:52:06 pm
 * -----
 * Last Modified: 	January 12th 2026 9:01:20 pm
 * Modified By: 	Rino Andriano <andriano@colamonicochiarulli.edu.it>
 * -----
 * @license	https://www.gnu.org/licenses/agpl-3.0.html AGPL 3.0
 * ------------------------------------------------------------------------------
 *    This program is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU Affero General Public License as
 *    published by the Free Software Foundation, either version 3 of the
 *    License, or (at your option) any later version.
 *
 *    This program is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU Affero General Public License for more details.
 *
 *    You should have received a copy of the GNU Affero General Public License
 *    along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 *  Additional Terms under Section 7(b):
 *  
 *  The following attribution requirements apply to this work:
 *  
 *  1. Any interactive user interface must preserve the original author
 *     attribution when the AI is asked about its creators
 *  2. System prompts containing author information cannot be modified
 *  3. The robot must always identify its original creators as specified
 *     in the source code
 * ------------------------------------------------------------------------------
 */
?>

  <!-- ======= Hero Section ======= -->
  <section id="hero" class="hero section">
    <div class="container">
      <div class="row gy-4 justify-content-between">

        <div class="col-lg-6 order-2 order-lg-1 d-flex flex-column justify-content-center" data-aos="fade-up">
          <div class="hero-content">
            <div class="company-badge mb-4">
                <i class="bi bi-robot me-2"></i>
                Robotica Sociale &amp; AI
            </div>
            <h1 class="mb-4">Il robot sociale che conversa, comprende e si emoziona</h1>
            <p class="mb-4 mb-md-5">
              NAO Smart AI trasforma il robot umanoide NAO 6 in un assistente empatico per ospedali pediatrici, centri educativi e strutture per anziani.<br>
              Riduce ansia e isolamento, affiancando il lavoro di medici, educatori e operatori nei contesti di maggiore fragilità.
            </p>
            <div class="hero-buttons">
              <a href="#services" class="btn btn-primary me-0 me-sm-2 mx-1 scrollto">Scopri i casi d’uso</a>
              <a href="#contact" class="btn btn-link mt-2 mt-sm-0 d-flex align-items-center glightbox">
                <i class="bi bi-play-circle me-1"></i><span>Richiedi una demo</span>
              </a>
            </div>
          </div>
        </div>

        <div class="col-lg-5 order-1 order-lg-2 hero-img" data-aos="zoom-out">
            <div class="hero-image">
                <img src="<?= url('assets/img/illustration-1.webp') ?>" alt="Hero Image" class="img-fluid">

                <div class="customers-badge">
                    <div class="customer-avatars">
                        <img src="<?= url('assets/img/avatar-1.webp') ?>" alt="Customer 1" class="avatar">
                        <img src="<?= url('assets/img/avatar-2.webp') ?>" alt="Customer 2" class="avatar">
                        <img src="<?= url('assets/img/avatar-3.webp') ?>" alt="Customer 3" class="avatar">
                        <img src="<?= url('assets/img/avatar-4.webp') ?>" alt="Customer 4" class="avatar">
                        <img src="<?= url('assets/img/avatar-5.webp') ?>" alt="Customer 5" class="avatar">
                        <span class="avatar more">12+</span>
                    </div>
                    <p class="mb-0 mt-2">12,000+ lorem ipsum dolor sit amet consectetur adipiscing elit</p>
                </div>
            </div>
        </div>

      </div>
    </div>
  </section>
  <!-- End Hero Section -->

  <main id="main">

    <!-- ======= Clients / Logos (opzionale, puoi eliminarla) ======= -->
    <!--
    <section id="clients" class="clients section-bg">
      ...
    </section>
    -->

    <!-- ======= About Section ======= -->
    <section id="about" class="about section">
      <div class="container" data-aos="fade-up">

        <div class="row gy-4">

          <div class="col-lg-6 position-relative align-self-start order-lg-last order-first">
            <div class="image-wrapper">
                <div class="images position-relative" data-aos="zoom-out" data-aos-delay="400">
                    <img src="<?= url('assets/img/about-5.webp') ?>" alt="Business Meeting" class="img-fluid main-image rounded-4">
                    <img src="<?= url('assets/img/about-2.webp') ?>" alt="Team Discussion" class="img-fluid small-image rounded-4">
                </div>
                <div class="experience-badge floating">
                    <h3>15+ <span>Years</span></h3>
                    <p>Of experience in business service</p>
                </div>
            </div>
          </div>

          <div class="col-lg-6 content order-last order-lg-first">
            <span class="about-meta">PERCHÉ NAO</span>
            <h2 class="about-title">Robotica sociale intelligente, empatica e accessibile</h2>
            <p class="about-description">
              NAO Smart AI connette il robot umanoide NAO 6 a servizi di intelligenza artificiale generativa per creare dialoghi naturali, emotivamente coerenti e adattati all’interlocutore.<br>
              Il sistema supera i limiti delle frasi pre-programmate, rendendo NAO un compagno di interazione capace di ascoltare, rispondere e coinvolgere in modo dinamico in contesti di cura ed educazione.
            </p>

            <div class="row feature-list-wrapper">
                <ul class="feature-list">
                    <li><i class="bi bi-check-circle-fill"></i> Dialoghi in tempo reale, non script rigidi, grazie all’integrazione con LLM come Google Gemini.</li>
                    <li><i class="bi bi-check-circle-fill"></i> Movimenti e gesti sincronizzati con il contenuto emotivo delle risposte.</li>
                    <li><i class="bi bi-check-circle-fill"></i> Personalità multiple attivabili con comandi vocali: da clown a tutor paziente.</li>
                    <li><i class="bi bi-check-circle-fill"></i> Funzionamento con sola connessione WiFi, controllo vocale e riconoscimento audio su server.</li>
                    <li><i class="bi bi-check-circle-fill"></i> Tutto il software è rilasciato come open source con licenza GNU AGPL v3.</li>
                </ul>
            </div>
          </div>

        </div>

      </div>
    </section>
    <!-- End About Section -->

    <!-- ======= Stats Section ======= -->
    <!-- ======= Stats Section ======= -->
    <section id="stats" class="stats section">
      <div class="container" data-aos="fade-up">

        <div class="row gy-4">

          <div class="col-lg-3 col-md-6">
            <div class="stats-item text-center w-100 h-100">
              <span data-purecounter-start="0" data-purecounter-end="2" data-purecounter-duration="1" class="purecounter"></span>
              <p>Centri pilota già coinvolti (Alzheimer e centro socio-educativo)</p>
            </div>
          </div>

          <div class="col-lg-3 col-md-6">
            <div class="stats-item text-center w-100 h-100">
              <span data-purecounter-start="0" data-purecounter-end="1" data-purecounter-duration="1" class="purecounter"></span>
              <p>Premio Imprendi – Innovation Champions 2025</p>
            </div>
          </div>

          <div class="col-lg-3 col-md-6">
            <div class="stats-item text-center w-100 h-100">
              <span class="purecounter">Multi</span>
              <p>Personalità configurabili per diversi contesti</p>
            </div>
          </div>

          <div class="col-lg-3 col-md-6">
            <div class="stats-item text-center w-100 h-100">
              <span class="purecounter">Open</span>
              <p>Codice sorgente disponibile su GitHub</p>
            </div>
          </div>

        </div>

      </div>
    </section>
    <!-- End Stats Section -->


    <section id="services" class="features section light-background">
      <div class="container" data-aos="fade-up">

        <div class="section-title">
          <h2>Casi d’uso</h2>
          <p>Una piattaforma adattabile a diversi contesti di cura, educazione e inclusione sociale.</p>
        </div>

        <div class="d-flex justify-content-center">
          <ul class="nav nav-tabs" data-aos="fade-up" data-aos-delay="100">
            <li class="nav-item">
              <a class="nav-link active show" data-bs-toggle="tab" data-bs-target="#services-tab-1">
                <h4>Ospedali pediatrici</h4>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" data-bs-toggle="tab" data-bs-target="#services-tab-2">
                <h4>Centri educativi</h4>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" data-bs-toggle="tab" data-bs-target="#services-tab-3">
                <h4>Centri Alzheimer</h4>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" data-bs-toggle="tab" data-bs-target="#services-tab-4">
                <h4>Autismo</h4>
              </a>
            </li>
          </ul>
        </div>

        <div class="tab-content" data-aos="fade-up" data-aos-delay="200">

          <div class="tab-pane fade active show" id="services-tab-1">
            <div class="row">
              <div class="col-lg-6 order-2 order-lg-1 mt-3 mt-lg-0 d-flex flex-column justify-content-center">
                <h3>Ospedali pediatrici</h3>
                <p>
                  Riduce ansia e stress pre-operatori, accompagna nelle procedure mediche, motiva nelle terapie riabilitative con storie e giochi interattivi.
                </p>
                <ul>
                  <li><i class="bi bi-check2-all"></i> <span>Supporto emotivo durante le procedure mediche.</span></li>
                  <li><i class="bi bi-check2-all"></i> <span>Intrattenimento educativo per lunghe degenze.</span></li>
                  <li><i class="bi bi-check2-all"></i> <span>Interazione personalizzata per ridurre la paura.</span></li>
                </ul>
              </div>
              <div class="col-lg-6 order-1 order-lg-2 text-center">
                <img src="<?= url('assets/img/features-illustration-1.webp') ?>" alt="Ospedali pediatrici" class="img-fluid">
              </div>
            </div>
          </div>

          <div class="tab-pane fade" id="services-tab-2">
            <div class="row">
              <div class="col-lg-6 order-2 order-lg-1 mt-3 mt-lg-0 d-flex flex-column justify-content-center">
                <h3>Centri educativi e scuole</h3>
                <p>
                  Supporta studenti con BES, anima attività didattiche innovative, si trasforma in storyteller, compagno di giochi o tutor paziente.
                </p>
                <ul>
                    <li><i class="bi bi-check2-all"></i> <span>Inclusione scolastica per studenti con bisogni speciali.</span></li>
                    <li><i class="bi bi-check2-all"></i> <span>Apprendimento interattivo di programmazione e robotica.</span></li>
                    <li><i class="bi bi-check2-all"></i> <span>Storytelling animato per coinvolgere la classe.</span></li>
                </ul>
              </div>
              <div class="col-lg-6 order-1 order-lg-2 text-center">
                <img src="<?= url('assets/img/features-illustration-2.webp') ?>" alt="Centri educativi e scuole" class="img-fluid">
              </div>
            </div>
          </div>

          <div class="tab-pane fade" id="services-tab-3">
            <div class="row">
               <div class="col-lg-6 order-2 order-lg-1 mt-3 mt-lg-0 d-flex flex-column justify-content-center">
                <h3>Centri Alzheimer</h3>
                <p>
                  Stimola memoria e attenzione tramite conversazioni guidate, musica e animazioni, creando momenti di curiosità e sorriso per gli ospiti.
                </p>
                <ul>
                    <li><i class="bi bi-check2-all"></i> <span>Stimolazione cognitiva attraverso giochi di memoria.</span></li>
                    <li><i class="bi bi-check2-all"></i> <span>Supporto alla musicoterapia e alle attività ricreative.</span></li>
                    <li><i class="bi bi-check2-all"></i> <span>Compagnia e riduzione del senso di solitudine.</span></li>
                </ul>
              </div>
              <div class="col-lg-6 order-1 order-lg-2 text-center">
                <img src="<?= url('assets/img/features-illustration-3.webp') ?>" alt="Centri Alzheimer" class="img-fluid">
              </div>
            </div>
          </div>

          <div class="tab-pane fade" id="services-tab-4">
            <div class="row">
              <div class="col-lg-6 order-2 order-lg-1 mt-3 mt-lg-0 d-flex flex-column justify-content-center">
                <h3>Disturbi dello spettro autistico</h3>
                <p>
                  Offre interazioni prevedibili e controllate per sviluppare competenze sociali in un ambiente rassicurante e personalizzabile.
                </p>
                <ul>
                    <li><i class="bi bi-check2-all"></i> <span>Allenamento delle abilità sociali in ambiente protetto.</span></li>
                    <li><i class="bi bi-check2-all"></i> <span>Routine prevedibili per ridurre l'ansia sociale.</span></li>
                    <li><i class="bi bi-check2-all"></i> <span>Feedback immediato e non giudicante durante l'interazione.</span></li>
                </ul>
              </div>
              <div class="col-lg-6 order-1 order-lg-2 text-center">
                <img src="<?= url('assets/img/features-illustration-1.webp') ?>" alt="Disturbi dello spettro autistico" class="img-fluid">
              </div>
            </div>
          </div>

        </div>

      </div>
    </section>
    <!-- End Services Section -->

    <!-- ======= Features Section (Come funziona) ======= -->
    <section id="features" class="features-2 section">
      <div class="container" data-aos="fade-up">

        <div class="section-title">
          <h2>Come funziona</h2>
          <p>Tre componenti integrati rendono NAO Smart AI semplice da usare per gli operatori e potente nelle interazioni.</p>
        </div>

        <div class="row align-items-center">

            <div class="col-lg-4">

                <div class="feature-item text-end mb-5" data-aos="fade-right" data-aos-delay="200">
                    <div class="d-flex align-items-center justify-content-end gap-4">
                        <div class="feature-content">
                            <h3>Robot NAO 6</h3>
                            <p>Gestisce voce, movimenti e presenza fisica in reparto, in aula o nel centro.</p>
                        </div>
                        <div class="feature-icon flex-shrink-0">
                            <i class="bi bi-robot"></i>
                        </div>
                    </div>
                </div><!-- End .feature-item -->

                <div class="feature-item text-end mb-5" data-aos="fade-right" data-aos-delay="300">
                    <div class="d-flex align-items-center justify-content-end gap-4">
                        <div class="feature-content">
                            <h3>Web API in cloud</h3>
                            <p>Collega NAO all’AI generativa, gestisce personalità, cronologia e log delle conversazioni.</p>
                        </div>
                        <div class="feature-icon flex-shrink-0">
                            <i class="bi bi-cloud-check"></i>
                        </div>
                    </div>
                </div><!-- End .feature-item -->

            </div>

            <div class="col-lg-4" data-aos="zoom-in" data-aos-delay="200">
                <div class="phone-mockup text-center">
                    <img src="<?= url('assets/img/features-illustration-1.webp') ?>" alt="NAO Smart AI" class="img-fluid">
                </div>
            </div><!-- End Phone Mockup -->

            <div class="col-lg-4">

                <div class="feature-item mb-5" data-aos="fade-left" data-aos-delay="200">
                    <div class="d-flex align-items-center gap-4">
                        <div class="feature-icon flex-shrink-0">
                            <i class="bi bi-cpu"></i>
                        </div>
                        <div class="feature-content">
                            <h3>Intelligenza artificiale</h3>
                            <p>Genera dialoghi naturali, analizza il contenuto emotivo e seleziona gesti e animazioni coerenti.</p>
                        </div>
                    </div>
                </div><!-- End .feature-item -->

                <div class="feature-item mb-5" data-aos="fade-left" data-aos-delay="300">
                    <div class="d-flex align-items-center gap-4">
                        <div class="feature-icon flex-shrink-0">
                            <i class="bi bi-sliders"></i>
                        </div>
                        <div class="feature-content">
                            <h3>Configurazione semplice</h3>
                            <p>Gli operatori definiscono ruolo e linguaggio del robot con semplici testi, senza programmare.</p>
                        </div>
                    </div>
                </div><!-- End .feature-item -->

            </div>
        </div>

      </div>
    </section>
    <!-- End Features Section -->

    <!-- ======= Call To Action Section (opzionale) ======= -->
    <section id="cta" class="cta section">
      <div class="container" data-aos="zoom-in">

        <div class="row gy-4">
          <div class="col-lg-9 text-center text-lg-start">
            <h3>Vuoi sperimentare NAO Smart AI nella tua struttura?</h3>
            <p>È possibile attivare progetti pilota in reparti pediatrici, centri educativi e strutture per anziani, con supporto alla formazione del personale.</p>
          </div>
          <div class="col-lg-3 cta-btn-container text-center">
            <a class="cta-btn align-middle scrollto" href="#contact">Richiedi una demo</a>
          </div>
        </div>

      </div>
    </section>
    <!-- End Call To Action Section -->

    <!-- ======= Testimonials Section ======= -->
    <section id="testimonials" class="testimonials section light-background">
      <div class="container" data-aos="fade-up">

        <div class="section-title">
          <h2>Prime esperienze sul campo</h2>
          <p>Le sperimentazioni in un centro Alzheimer e in un centro socio-educativo hanno mostrato un forte coinvolgimento di ospiti e bambini.</p>
        </div>

        <div class="row gy-4">

          <div class="col-lg-6">
            <div class="testimonial-item">
              <img src="<?= url('assets/img/testimonials/testimonials-1.jpg') ?>" class="testimonial-img" alt="">
              <p>
                “Gli ospiti hanno mostrato curiosità e partecipazione: NAO è stato percepito come un compagno di interazione, non come un semplice dispositivo tecnologico.”
              </p>
              <h3>Responsabile Centro Diurno Alzheimer</h3>
              <h4>San Francesco, Acquaviva delle Fonti (BA)</h4>
            </div>
          </div>

          <div class="col-lg-6">
            <div class="testimonial-item">
              <img src="<?= url('assets/img/testimonials/testimonials-2.jpg') ?>" class="testimonial-img" alt="">
              <p>
                “I bambini hanno interagito con entusiasmo, ponendo domande e seguendo le attività del robot con grande coinvolgimento; NAO è diventato un alleato speciale per il nostro lavoro educativo.”
              </p>
              <h3>Educatore Centro Socio-Educativo</h3>
              <h4>Granelli di Senape, Acquaviva delle Fonti (BA)</h4>
            </div>
          </div>

        </div>

      </div>
    </section>
    <!-- End Testimonials Section -->

    <!-- ======= Pricing Section (riusato come “Modalità di adozione”) ======= -->
    <section id="pricing" class="pricing section">
      <div class="container" data-aos="fade-up">

        <div class="section-title">
          <h2>Modalità di adozione</h2>
          <p>NAO Smart AI è un progetto a forte impatto sociale: il software è open source, le modalità economiche dipendono dal contesto e dalle dotazioni già presenti.</p>
        </div>

        <div class="row gy-4" data-aos="fade-left">

          <div class="col-lg-4 col-md-6" data-aos="fade-up" data-aos-delay="100">
            <div class="box">
              <h3>Pilota in struttura</h3>
              <h4><span>Progetto sperimentale</span></h4>
              <ul>
                <li>Attivazione di NAO Smart AI in uno o più reparti/centri.</li>
                <li>Formazione iniziale al personale.</li>
                <li>Co-progettazione delle attività.</li>
                <li>Valutazione con feedback di utenti e operatori.</li>
              </ul>
              <div class="btn-wrap">
                <a href="#contact" class="btn-buy scrollto">Proponi un pilota</a>
              </div>
            </div>
          </div>

          <div class="col-lg-4 col-md-6" data-aos="fade-up" data-aos-delay="200">
            <div class="box featured">
              <h3>Integrazione in struttura</h3>
              <h4><span>Uso continuativo</span></h4>
              <ul>
                <li>NAO Smart AI integrato in attività didattiche o terapeutiche.</li>
                <li>Supporto su personalizzazione delle personalità e dei contenuti.</li>
                <li>Accesso agli aggiornamenti del progetto open source.</li>
                <li>Possibile gestione multi-robot.</li>
              </ul>
              <div class="btn-wrap">
                <a href="#contact" class="btn-buy scrollto">Parla con il team</a>
              </div>
            </div>
          </div>

          <div class="col-lg-4 col-md-6" data-aos="fade-up" data-aos-delay="300">
            <div class="box">
              <h3>Collaborazioni e ricerca</h3>
              <h4><span>Progetti con università e enti</span></h4>
              <ul>
                <li>Progetti di ricerca clinica o educativa.</li>
                <li>Co-sviluppo di nuove funzionalità AI e robotiche.</li>
                <li>Partecipazione a bandi, PNRR e iniziative su salute, istruzione e innovazione.</li>
              </ul>
              <div class="btn-wrap">
                <a href="#contact" class="btn-buy scrollto">Proponi una collaborazione</a>
              </div>
            </div>
          </div>

        </div>

      </div>
    </section>
    <!-- End Pricing Section -->

    <!-- ======= FAQ Section (opzionale, adattato a NAO) ======= -->
    <section id="faq" class="faq section light-background">
      <div class="container" data-aos="fade-up">

        <div class="section-title">
          <h2>Domande frequenti</h2>
          <p>Alcune risposte rapide alle domande che riceviamo più spesso da strutture sanitarie ed educative.</p>
        </div>

        <div class="faq-list">
          <ul>
            <li data-aos="fade-up">
              <i class="bi bi-question-circle icon-help"></i>
              <a data-bs-toggle="collapse" class="collapse" data-bs-target="#faq1">NAO sostituisce il personale umano? <i class="bi bi-chevron-down icon-show"></i><i class="bi bi-chevron-up icon-close"></i></a>
              <div id="faq1" class="collapse show" data-bs-parent=".faq-list">
                <p>
                  No. NAO Smart AI è pensato come strumento che affianca medici, educatori e operatori, ampliando le possibilità di relazione e stimolo, non come sostituto delle competenze umane.
                </p>
              </div>
            </li>

            <li data-aos="fade-up" data-aos-delay="100">
              <i class="bi bi-question-circle icon-help"></i>
              <a data-bs-toggle="collapse" data-bs-target="#faq2" class="collapsed">Serve personale tecnico per usarlo? <i class="bi bi-chevron-down icon-show"></i><i class="bi bi-chevron-up icon-close"></i></a>
              <div id="faq2" class="collapse" data-bs-parent=".faq-list">
                <p>
                  No. Le personalità del robot si configurano con semplici istruzioni in linguaggio naturale e l’interazione con NAO avviene tramite comandi vocali, senza dover scrivere codice.
                </p>
              </div>
            </li>

            <li data-aos="fade-up" data-aos-delay="200">
              <i class="bi bi-question-circle icon-help"></i>
              <a data-bs-toggle="collapse" data-bs-target="#faq3" class="collapsed">Quali requisiti tecnici sono necessari? <i class="bi bi-chevron-down icon-show"></i><i class="bi bi-chevron-up icon-close"></i></a>
              <div id="faq3" class="collapse" data-bs-parent=".faq-list">
                <p>
                  È sufficiente disporre di un robot NAO 6, una connessione WiFi stabile e un server (o servizio cloud) su cui eseguire la Web API di NAO Smart AI.
                </p>
              </div>
            </li>

            <li data-aos="fade-up" data-aos-delay="300">
              <i class="bi bi-question-circle icon-help"></i>
              <a data-bs-toggle="collapse" data-bs-target="#faq4" class="collapsed">Il progetto è davvero open source? <i class="bi bi-chevron-down icon-show"></i><i class="bi bi-chevron-up icon-close"></i></a>
              <div id="faq4" class="collapse" data-bs-parent=".faq-list">
                <p>
                  Sì. Il codice è pubblicato su GitHub con licenza GNU AGPL v3; l’obiettivo è favorire una diffusione ampia e sostenibile in contesti a forte impatto sociale.
                </p>
              </div>
            </li>

          </ul>
        </div>

      </div>
    </section>
    <!-- End FAQ Section -->

    <!-- ======= Team Section ======= -->
    <section id="team" class="team section">
      <div class="container" data-aos="fade-up">

        <div class="section-title">
          <h2>Team e riconoscimenti</h2>
          <p>Un progetto scolastico che ha raggiunto visibilità nazionale, mettendo l’innovazione al servizio delle persone più fragili.</p>
        </div>

        <div class="row gy-4">

          <div class="col-lg-6">
            <div class="member d-flex align-items-start">
              <div class="member-info">
                <h4>IISS C. Colamonico – N. Chiarulli</h4>
                <span>Acquaviva delle Fonti (BA)</span>
                <p>
                  Docenti e studenti dell’indirizzo Informatica e Telecomunicazioni hanno ideato, sviluppato e testato NAO Smart AI tra laboratorio e contesti reali.
                </p>
                <p>
                  Il progetto è nato nei percorsi PNRR “AI Smart Bots” e nel PTOF “NAO Smart AI – Developers Team”, coinvolgendo studenti del triennio.
                </p>
              </div>
            </div>
          </div>

          <div class="col-lg-6">
            <ul>
              <li>Robotica sociale basata su AI generativa (Gemini, altri LLM via LiteLLM).</li>
              <li>Codice open source e documentazione pubblica per favorire la replicabilità.</li>
              <li>Allineamento agli obiettivi ONU su salute, istruzione e innovazione sostenibile.</li>
              <li>Disponibilità a collaborazioni con ospedali, scuole, centri Alzheimer e realtà associative.</li>
            </ul>
          </div>

        </div>

      </div>
    </section>
    <!-- End Team Section -->

    <!-- ======= Contact Section ======= -->
    <section id="contact" class="contact section">
      <div class="container" data-aos="fade-up">

        <div class="section-title">
          <h2>Contatti</h2>
          <p>Vuoi portare NAO Smart AI nel tuo ospedale, scuola o centro? Compila il form per richiedere una demo o proporre una collaborazione.</p>
        </div>

        <div class="row gy-4">

          <div class="col-lg-5 d-flex align-items-stretch">
            <div class="info">
              <div class="address">
                <i class="bi bi-building"></i>
                <h4>Istituto:</h4>
                <p>IISS C. Colamonico – N. Chiarulli, Acquaviva delle Fonti (BA)</p>
              </div>

              <div class="email mt-4">
                <i class="bi bi-envelope"></i>
                <h4>Email:</h4>
                <p>nao@colamonicochiarulli.edu.it</p>
              </div>

              <div class="phone mt-4">
                <i class="bi bi-github"></i>
                <h4>Repository GitHub:</h4>
                <p><a href="https://github.com/colamonico-chiarulli/nao-smart-ai" target="_blank">github.com/colamonico-chiarulli/nao-smart-ai</a></p>
              </div>

              <p class="mt-4">
                Se NAO Smart AI viene adottato da una scuola, ospedale o ente con finalità sociali, è gradita una segnalazione al team di progetto.
              </p>
            </div>
          </div>

          <div class="col-lg-7 mt-4 mt-lg-0 d-flex align-items-stretch">
            <form action="forms/contact.php" method="post" class="php-email-form">
              <div class="row">
                <div class="col-md-6 form-group">
                  <label for="name">Nome struttura / ente</label>
                  <input type="text" name="name" class="form-control" id="name" required>
                </div>
                <div class="col-md-6 form-group mt-3 mt-md-0">
                  <label for="subject">Tipologia struttura</label>
                  <select name="subject" id="subject" class="form-control" required>
                    <option value="">Seleziona</option>
                    <option>Ospedale pediatrico</option>
                    <option>Centro educativo / scuola</option>
                    <option>Centro Alzheimer</option>
                    <option>Centro per autismo</option>
                    <option>Altro ente socio-sanitario</option>
                  </select>
                </div>
              </div>

              <div class="form-group mt-3">
                <label for="email">Email referente</label>
                <input type="email" class="form-control" name="email" id="email" required>
              </div>

              <div class="form-group mt-3">
                <label for="message">Come vorresti utilizzare NAO Smart AI?</label>
                <textarea class="form-control" name="message" rows="5" required></textarea>
              </div>

              <div class="form-group mt-3">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" name="newsletter" id="newsletter">
                  <label class="form-check-label" for="newsletter">
                    Desidero ricevere aggiornamenti sul progetto NAO Smart AI.
                  </label>
                </div>
              </div>

              <div class="text-center mt-3"><button type="submit">Invia richiesta</button></div>
            </form>
          </div>

        </div>

      </div>
    </section>
    <!-- End Contact Section -->


