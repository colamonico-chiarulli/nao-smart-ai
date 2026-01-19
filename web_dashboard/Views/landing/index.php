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
        
      <div class="row stats-row gy-4 mt-5" data-aos="fade-up" data-aos-delay="500">
        <div class="col-lg-3 col-md-6">
          <div class="stat-item">
            <div class="stat-icon">
              <i class="bi bi-trophy"></i>
            </div>
            <div class="stat-content">
              <h4>2 Centri pilota</h4>
              <p class="mb-0">Alzheimer e centro educativo</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-md-6">
          <div class="stat-item">
            <div class="stat-icon">
              <i class="bi bi-award"></i>
            </div>
            <div class="stat-content">
              <h4>1° Premio</h4>
              <p class="mb-0">Innovation Champions 2025</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-md-6">
          <div class="stat-item">
            <div class="stat-icon">
              <i class="bi bi-graph-up"></i>
            </div>
            <div class="stat-content">
              <h4>Multi Ruolo</h4>
              <p class="mb-0">Personalità adattabili</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-md-6">
          <div class="stat-item">
            <div class="stat-icon">
              <i class="bi bi-github"></i>
            </div>
            <div class="stat-content">
              <h4>Open Source</h4>
              <p class="mb-0">Codice disponibile su GitHub</p>
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

    <!-- ======= Call To Action Section ======= -->
    <section id="call-to-action" class="call-to-action section dark-background">

      <div class="container" data-aos="fade-up" data-aos-delay="100">

        <div class="row content justify-content-center align-items-center position-relative">
          <div class="col-lg-8 mx-auto text-center">
            <h2 class="display-4 mb-4">Vuoi sperimentare NAO Smart AI nella tua struttura?</h2>
            <p class="mb-4">È possibile attivare progetti pilota in reparti pediatrici, centri educativi e strutture per anziani, con supporto alla formazione del personale.</p>
            <a href="#contact" class="btn btn-cta">Richiedi una demo</a>
          </div>

          <!-- Abstract Background Elements -->
          <div class="shape shape-1">
            <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
              <path d="M47.1,-57.1C59.9,-45.6,68.5,-28.9,71.4,-10.9C74.2,7.1,71.3,26.3,61.5,41.1C51.7,55.9,35,66.2,16.9,69.2C-1.3,72.2,-21,67.8,-36.9,57.9C-52.8,48,-64.9,32.6,-69.1,15.1C-73.3,-2.4,-69.5,-22,-59.4,-37.1C-49.3,-52.2,-32.8,-62.9,-15.7,-64.9C1.5,-67,34.3,-68.5,47.1,-57.1Z" transform="translate(100 100)"></path>
            </svg>
          </div>

          <div class="shape shape-2">
            <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
              <path d="M41.3,-49.1C54.4,-39.3,66.6,-27.2,71.1,-12.1C75.6,3,72.4,20.9,63.3,34.4C54.2,47.9,39.2,56.9,23.2,62.3C7.1,67.7,-10,69.4,-24.8,64.1C-39.7,58.8,-52.3,46.5,-60.1,31.5C-67.9,16.4,-70.9,-1.4,-66.3,-16.6C-61.8,-31.8,-49.7,-44.3,-36.3,-54C-22.9,-63.7,-8.2,-70.6,3.6,-75.1C15.4,-79.6,28.2,-58.9,41.3,-49.1Z" transform="translate(100 100)"></path>
            </svg>
          </div>

          <!-- Dot Pattern Groups -->
          <div class="dots dots-1">
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <pattern id="dot-pattern" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
                <circle cx="2" cy="2" r="2" fill="currentColor"></circle>
              </pattern>
              <rect width="100" height="100" fill="url(#dot-pattern)"></rect>
            </svg>
          </div>

          <div class="dots dots-2">
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <pattern id="dot-pattern-2" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
                <circle cx="2" cy="2" r="2" fill="currentColor"></circle>
              </pattern>
              <rect width="100" height="100" fill="url(#dot-pattern-2)"></rect>
            </svg>
          </div>

          <div class="shape shape-3">
            <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
              <path d="M43.3,-57.1C57.4,-46.5,71.1,-32.6,75.3,-16.2C79.5,0.2,74.2,19.1,65.1,35.3C56,51.5,43.1,65,27.4,71.7C11.7,78.4,-6.8,78.3,-23.9,72.4C-41,66.5,-56.7,54.8,-65.4,39.2C-74.1,23.6,-75.8,4,-71.7,-13.2C-67.6,-30.4,-57.7,-45.2,-44.3,-56.1C-30.9,-67,-15.5,-74,0.7,-74.9C16.8,-75.8,33.7,-70.7,43.3,-57.1Z" transform="translate(100 100)"></path>
            </svg>
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

        <div class="row g-4 justify-content-center">

          <!-- Pilota in struttura -->
          <div class="col-lg-4" data-aos="fade-up" data-aos-delay="100">
            <div class="pricing-card">
              <h3>Pilota in struttura</h3>
              <p class="description">Progetto sperimentale</p>

              <h4>Cosa include:</h4>
              <ul class="features-list">
                <li>
                    <i class="bi bi-check-circle-fill"></i>
                    Attivazione NAO Smart AI in reparti/centri
                </li>
                <li>
                    <i class="bi bi-check-circle-fill"></i>
                    Formazione iniziale al personale
                </li>
                <li>
                    <i class="bi bi-check-circle-fill"></i>
                    Co-progettazione delle attività
                </li>
                <li>
                    <i class="bi bi-check-circle-fill"></i>
                    Valutazione con feedback utenti
                </li>
              </ul>

              <a href="#contact" class="btn btn-primary">
                  Proponi un pilota
                  <i class="bi bi-arrow-right"></i>
              </a>
            </div>
          </div>

          <!-- Integrazione in struttura (Popular) -->
          <div class="col-lg-4" data-aos="fade-up" data-aos-delay="200">
            <div class="pricing-card popular">
              <h3>Integrazione in struttura</h3>
              <p class="description">Uso continuativo</p>

              <h4>Cosa include:</h4>
              <ul class="features-list">
                <li>
                    <i class="bi bi-check-circle-fill"></i>
                    Integrazione in attività didattiche
                </li>
                <li>
                    <i class="bi bi-check-circle-fill"></i>
                    Supporto configurazione personalità
                </li>
                <li>
                    <i class="bi bi-check-circle-fill"></i>
                    Accesso aggiornamenti open source
                </li>
                <li>
                    <i class="bi bi-check-circle-fill"></i>
                    Possibile gestione multi-robot
                </li>
              </ul>

              <a href="#contact" class="btn btn-light">
                  Parla con il team
                  <i class="bi bi-arrow-right"></i>
              </a>
            </div>
          </div>

          <!-- Collaborazioni e ricerca -->
          <div class="col-lg-4" data-aos="fade-up" data-aos-delay="300">
            <div class="pricing-card">
              <h3>Collaborazioni e ricerca</h3>
              <p class="description">Progetti con università e enti</p>

              <h4>Cosa include:</h4>
              <ul class="features-list">
                <li>
                    <i class="bi bi-check-circle-fill"></i>
                    Ricerca clinica o educativa
                </li>
                <li>
                    <i class="bi bi-check-circle-fill"></i>
                    Co-sviluppo nuove funzionalità
                </li>
                <li>
                    <i class="bi bi-check-circle-fill"></i>
                    Partecipazione a bandi e PNRR
                </li>
                <li>
                    <i class="bi bi-check-circle-fill"></i>
                    Innovazione su salute e istruzione
                </li>
              </ul>

              <a href="#contact" class="btn btn-primary">
                  Proponi collaborazione
                  <i class="bi bi-arrow-right"></i>
              </a>
            </div>
          </div>

        </div>

      </div>
    </section>
    <!-- End Pricing Section -->

    <!-- ======= FAQ Section (opzionale, adattato a NAO) ======= -->
    <section id="faq" class="faq-9 faq section light-background">
      <div class="container">
        <div class="row">

            <div class="col-lg-5" data-aos="fade-up">
                <h2 class="faq-title">Domande frequenti</h2>
                <p class="faq-description">Alcune risposte rapide alle domande che riceviamo più spesso da strutture sanitarie ed educative.</p>
                <div class="faq-arrow d-none d-lg-block" data-aos="fade-up" data-aos-delay="200">
                    <svg class="faq-arrow" width="200" height="211" viewBox="0 0 200 211" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M198.804 194.488C189.279 189.596 179.529 185.52 169.407 182.07L169.384 182.049C169.227 181.994 169.07 181.939 168.912 181.884C166.669 181.139 165.906 184.546 167.669 185.615C174.053 189.473 182.761 191.837 189.146 195.695C156.603 195.912 119.781 196.591 91.266 179.049C62.5221 161.368 48.1094 130.695 56.934 98.891C84.5539 98.7247 112.556 84.0176 129.508 62.667C136.396 53.9724 146.193 35.1448 129.773 30.2717C114.292 25.6624 93.7109 41.8875 83.1971 51.3147C70.1109 63.039 59.63 78.433 54.2039 95.0087C52.1221 94.9842 50.0776 94.8683 48.0703 94.6608C30.1803 92.8027 11.2197 83.6338 5.44902 65.1074C-1.88449 41.5699 14.4994 19.0183 27.9202 1.56641C28.6411 0.625793 27.2862 -0.561638 26.5419 0.358501C13.4588 16.4098 -0.221091 34.5242 0.896608 56.5659C1.8218 74.6941 14.221 87.9401 30.4121 94.2058C37.7076 97.0203 45.3454 98.5003 53.0334 98.8449C47.8679 117.532 49.2961 137.487 60.7729 155.283C87.7615 197.081 139.616 201.147 184.786 201.155L174.332 206.827C172.119 208.033 174.345 211.287 176.537 210.105C182.06 207.125 187.582 204.122 193.084 201.144C193.346 201.147 195.161 199.887 195.423 199.868C197.08 198.548 193.084 201.144 195.528 199.81C196.688 199.192 197.846 198.552 199.006 197.935C200.397 197.167 200.007 195.087 198.804 194.488ZM60.8213 88.0427C67.6894 72.648 78.8538 59.1566 92.1207 49.0388C98.8475 43.9065 106.334 39.2953 114.188 36.1439C117.295 34.8947 120.798 33.6609 124.168 33.635C134.365 33.5511 136.354 42.9911 132.638 51.031C120.47 77.4222 86.8639 93.9837 58.0983 94.9666C58.8971 92.6666 59.783 90.3603 60.8213 88.0427Z" fill="currentColor"></path>
                    </svg>
                </div>
            </div>

            <div class="col-lg-7" data-aos="fade-up" data-aos-delay="300">
                <div class="faq-container">

                    <div class="faq-item faq-active">
                        <h3>NAO sostituisce il personale umano?</h3>
                        <div class="faq-content">
                            <p>No. NAO Smart AI è pensato come strumento che affianca medici, educatori e operatori, ampliando le possibilità di relazione e stimolo, non come sostituto delle competenze umane.</p>
                        </div>
                        <i class="faq-toggle bi bi-chevron-right"></i>
                    </div><!-- End Faq item-->

                    <div class="faq-item">
                        <h3>Serve personale tecnico per usarlo?</h3>
                        <div class="faq-content">
                            <p>No. Le personalità del robot si configurano con semplici istruzioni in linguaggio naturale e l’interazione con NAO avviene tramite comandi vocali, senza dover scrivere codice.</p>
                        </div>
                        <i class="faq-toggle bi bi-chevron-right"></i>
                    </div><!-- End Faq item-->

                    <div class="faq-item">
                        <h3>Quali requisiti tecnici sono necessari?</h3>
                        <div class="faq-content">
                            <p>È sufficiente disporre di un robot NAO 6, una connessione WiFi stabile e un server (o servizio cloud) su cui eseguire la Web API di NAO Smart AI.</p>
                        </div>
                        <i class="faq-toggle bi bi-chevron-right"></i>
                    </div><!-- End Faq item-->

                    <div class="faq-item">
                        <h3>Il progetto è davvero open source?</h3>
                        <div class="faq-content">
                            <p>Sì. Il codice è pubblicato su GitHub con licenza GNU AGPL v3; l’obiettivo è favorire una diffusione ampia e sostenibile in contesti a forte impatto sociale.</p>
                        </div>
                        <i class="faq-toggle bi bi-chevron-right"></i>
                    </div><!-- End Faq item-->

                </div>
            </div>

        </div>
      </div>
    </section>
    <!-- End FAQ Section -->

    <!-- ======= Team Section (con layout Services) ======= -->
    <section id="team" class="services section">
      <div class="container" data-aos="fade-up">

        <div class="section-title">
          <h2>Team e riconoscimenti</h2>
          <p>Un progetto scolastico che ha raggiunto visibilità nazionale, mettendo l’innovazione al servizio delle persone più fragili.</p>
        </div>

        <div class="row g-4">

          <div class="col-lg-6" data-aos="fade-up" data-aos-delay="100">
            <div class="service-card d-flex">
              <div class="icon flex-shrink-0">
                <i class="bi bi-buildings"></i>
              </div>
              <div>
                <h3>IISS C. Colamonico – N. Chiarulli</h3>
                <p>Acquaviva delle Fonti (BA)</p>
                <p>Docenti e studenti dell’indirizzo Informatica e Telecomunicazioni hanno ideato, sviluppato e testato NAO Smart AI tra laboratorio e contesti reali.</p>
                <p>Il progetto è nato nei percorsi PNRR “AI Smart Bots” e nel PTOF “NAO Smart AI – Developers Team”, coinvolgendo studenti del triennio.</p>
              </div>
            </div>
          </div>

          <div class="col-lg-6" data-aos="fade-up" data-aos-delay="200">
             <div class="service-card d-flex">
              <div class="icon flex-shrink-0">
                <i class="bi bi-award"></i>
              </div>
              <div>
                <h3>Obiettivi e Tecnologie</h3>
                <ul>
                  <li>Robotica sociale basata su AI generativa (Gemini, altri LLM via LiteLLM).</li>
                  <li>Codice open source e documentazione pubblica per favorire la replicabilità.</li>
                  <li>Allineamento agli obiettivi ONU su salute, istruzione e innovazione sostenibile.</li>
                  <li>Disponibilità a collaborazioni con ospedali, scuole, centri Alzheimer e realtà associative.</li>
                </ul>
              </div>
            </div>
          </div>

        </div>

      </div>
    </section>
    <!-- End Team Section -->

    <!-- ======= Contact Section ======= -->
    <section id="contact" class="contact section light-background">
      <div class="container" data-aos="fade-up">

        <div class="section-title">
          <h2>Contatti</h2>
          <p>Vuoi portare NAO Smart AI nel tuo ospedale, scuola o centro? Compila il form per richiedere una demo o proporre una collaborazione.</p>
        </div>

        <div class="row g-4 g-lg-5">

          <div class="col-lg-5">
              <div class="info-box" data-aos="fade-up" data-aos-delay="200">
                  <h3>Recapiti</h3>
                  <p>Siamo a disposizione per informazioni tecniche, didattiche e amministrative.</p>

                  <div class="info-item" data-aos="fade-up" data-aos-delay="300">
                      <div class="icon-box">
                          <i class="bi bi-geo-alt"></i>
                      </div>
                      <div class="content">
                          <h4>Istituto</h4>
                          <p>IISS C. Colamonico – N. Chiarulli</p>
                          <p>Acquaviva delle Fonti (BA)</p>
                      </div>
                  </div>

                  <div class="info-item" data-aos="fade-up" data-aos-delay="400">
                      <div class="icon-box">
                          <i class="bi bi-envelope"></i>
                      </div>
                      <div class="content">
                          <h4>Email</h4>
                          <p>nao@colamonicochiarulli.edu.it</p>
                      </div>
                  </div>

                  <div class="info-item" data-aos="fade-up" data-aos-delay="500">
                      <div class="icon-box">
                          <i class="bi bi-github"></i>
                      </div>
                      <div class="content">
                          <h4>Repository GitHub</h4>
                          <p><a href="https://github.com/colamonico-chiarulli/nao-smart-ai" target="_blank">colamonico-chiarulli/nao-smart-ai</a></p>
                      </div>
                  </div>
              </div>
          </div>

          <div class="col-lg-7">
            <div class="contact-form" data-aos="fade-up" data-aos-delay="300">
                <h3>Inviaci un messaggio</h3>
                <p>Compila il modulo sottostante per essere ricontattato dal nostro team.</p>

                <form action="forms/contact.php" method="post" class="php-email-form" data-aos="fade-up" data-aos-delay="200">
                  <div class="row gy-4">
                    <div class="col-md-6 form-group">
                      <input type="text" name="name" class="form-control" id="name" placeholder="Nome struttura / ente" required>
                    </div>
                    <div class="col-md-6 form-group">
                      <select name="subject" id="subject" class="form-control" required>
                        <option value="">Tipologia struttura...</option>
                        <option>Ospedale pediatrico</option>
                        <option>Centro educativo / scuola</option>
                        <option>Centro Alzheimer</option>
                        <option>Centro per autismo</option>
                        <option>Altro ente socio-sanitario</option>
                      </select>
                    </div>

                    <div class="col-md-12 form-group">
                        <input type="email" class="form-control" name="email" id="email" placeholder="Email referente" required>
                    </div>

                    <div class="col-md-12 form-group">
                      <textarea class="form-control" name="message" rows="5" placeholder="Come vorresti utilizzare NAO Smart AI?" required></textarea>
                    </div>

                    <div class="col-md-12 form-group">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" name="newsletter" id="newsletter">
                            <label class="form-check-label" for="newsletter">
                                Desidero ricevere aggiornamenti sul progetto NAO Smart AI.
                            </label>
                        </div>
                    </div>

                    <div class="col-12 text-center">
                        <div class="loading">Loading</div>
                        <div class="error-message"></div>
                        <div class="sent-message">Your message has been sent. Thank you!</div>
                        <button type="submit" class="btn">Invia richiesta</button>
                    </div>

                  </div>
                </form>

            </div>
          </div>

        </div>

      </div>
    </section>
    <!-- End Contact Section -->


