<?php
/**
 * File: src/Core/View.php
 * @package NAO-Smart-AI
 * @author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
 *
 * Created Date: Tuesday, December 17th 2025, 10:52:06 pm
 * -----
 * Last Modified: 	December 17th 2025 10:52:06 pm
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


namespace App\Core;

/**
 * Gestisce il rendering delle viste HTML.
 */
class View
{
    /**
     * Include il file della vista specificata e lo inserisce nel layout principale.
     * 
     * @param string $view Nome della vista (es. 'contact/list').
     * @param array $data Array associativo di dati da passare alla vista.
     * @throws Exception Se il file non esiste.
     */
    public static function render($view, $data = [], $layout = 'layout_dashboard')
    {
        // Estrai i dati per renderli disponibili come variabili nella vista
        extract($data);

        // Percorso base delle viste
        $viewFile = __DIR__ . '/../../Views/' . $view . '.php';

        if (file_exists($viewFile)) {
            // Avvia buffer di output
            ob_start();
            require $viewFile;
            $content = ob_get_clean();

            // Include il layout specificato (se non è nullo)
            if ($layout) {
                $layoutFile = __DIR__ . '/../../Views/' . $layout . '.php';
                if (file_exists($layoutFile)) {
                    require $layoutFile;
                } else {
                    throw new \Exception("Layout non trovato: $layoutFile");
                }
            } else {
                echo $content;
            }

        } else {
            throw new \Exception("Vista non trovata: $viewFile");
        }
    }

    /**
     * Renderizza senza layout (per parziali o ajax).
     * 
     * @param string $view Nome della vista.
     * @param array $data Dati da passare.
     */
    public static function renderPartial($view, $data = [])
    {
        extract($data);
        $viewFile = __DIR__ . '/../../Views/' . $view . '.php';
        if (file_exists($viewFile)) {
            require $viewFile;
        }
    }
}
