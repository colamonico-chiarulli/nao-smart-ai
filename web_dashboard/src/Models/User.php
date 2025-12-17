<?php
/**
 * File: src/Models/User.php
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


namespace App\Models;

use App\Core\Database;

/**
 * Model per la gestione degli Utenti nel database.
 */
class User
{
    private $db;

    /**
     * Costruttore. Ottiene l'istanza del database.
     */
    public function __construct()
    {
        $this->db = Database::getInstance()->getConnection();
    }

    /**
     * Recupera un singolo utente per ID.
     * 
     * @param int $id ID dell'utente.
     * @return array|null Dati dell'utente o null se non trovato.
     */
    public function getById($id)
    {
        $stmt = $this->db->prepare("SELECT * FROM users WHERE id = ?");
        $stmt->bind_param("i", $id);
        $stmt->execute();
        $result = $stmt->get_result();
        return $result->fetch_assoc();
    }

    /**
     * Crea un nuovo utente.
     * 
     * @param array $data Dati dell'utente validati.
     * @return bool True se successo, False altrimenti.
     */
    public function create($data)
    {
        $sql = "INSERT INTO users (last_name, first_name, organization, email, password, phone, role) VALUES (?, ?, ?, ?, ?, ?, ?)";
        $stmt = $this->db->prepare($sql);

        // Hash password before saving if not already hashed? 
        // Controller should handle hashing ideally, but let's assume passed data has password.
        // Wait, for security, password hashing should be explicit. 
        // I will assume the controller passes the raw password and I hash it here OR controller hashes it.
        // Let's assume controller does the hashing to keep model simple or vice versa?
        // Better: Controller prepares data. But let's clarify.
        // I will assume data['password'] is ALREADY HASHED or needs to be hashed.
        // Given PHP best practices, usually logic is in Controller or Service. Model just saves.

        $stmt->bind_param(
            "sssssss",
            $data['last_name'],
            $data['first_name'],
            $data['organization'],
            $data['email'],
            $data['password'],
            $data['phone'],
            $data['role']
        );
        return $stmt->execute();
    }

    /**
     * Aggiorna un utente esistente.
     * 
     * @param int $id ID dell'utente.
     * @param array $data Dati aggiornati.
     * @return bool True se successo.
     */
    public function update($id, $data)
    {
        // If password is provided (not empty), update it. Else keep old.
        // This makes the query dynamic.

        if (!empty($data['password'])) {
            $sql = "UPDATE users SET last_name=?, first_name=?, organization=?, email=?, password=?, phone=?, role=? WHERE id=?";
            $stmt = $this->db->prepare($sql);
            $stmt->bind_param(
                "sssssssi",
                $data['last_name'],
                $data['first_name'],
                $data['organization'],
                $data['email'],
                $data['password'],
                $data['phone'],
                $data['role'],
                $id
            );
        } else {
            $sql = "UPDATE users SET last_name=?, first_name=?, organization=?, email=?, phone=?, role=? WHERE id=?";
            $stmt = $this->db->prepare($sql);
            $stmt->bind_param(
                "ssssssi",
                $data['last_name'],
                $data['first_name'],
                $data['organization'],
                $data['email'],
                $data['phone'],
                $data['role'],
                $id
            );
        }

        return $stmt->execute();
    }

    /**
     * Cancella un utente.
     * 
     * @param int $id ID dell'utente.
     * @return bool True se successo.
     */
    public function delete($id)
    {
        $stmt = $this->db->prepare("DELETE FROM users WHERE id = ?");
        $stmt->bind_param("i", $id);
        return $stmt->execute();
    }

    /**
     * Conta il numero totale di utenti, eventualmente filtrati.
     * 
     * @param string $search Filtro di ricerca per cognome.
     * @return int Numero totale di utenti.
     */
    public function countAll($search = '')
    {
        $sql = "SELECT COUNT(*) as total FROM users";
        if (!empty($search)) {
            $sql .= " WHERE last_name LIKE ? OR first_name LIKE ? OR email LIKE ?";
        }

        $stmt = $this->db->prepare($sql);

        if (!empty($search)) {
            $wildcard = "%$search%";
            $stmt->bind_param("sss", $wildcard, $wildcard, $wildcard);
        }

        $stmt->execute();
        $result = $stmt->get_result();
        $row = $result->fetch_assoc();
        return (int) $row['total'];
    }

    /**
     * Recupera gli utenti per la pagina corrente con ordinamento e filtro.
     * 
     * @param int $limit Numero di utenti per pagina.
     * @param int $offset Offset per la query.
     * @param string $sortCol Colonna per ordinamento.
     * @param string $sortOrder Ordine (ASC, DESC).
     * @param string $search Filtro di ricerca.
     * @return array Array di utenti.
     */
    public function getPaginated($limit = 10, $offset = 0, $sortCol = 'last_name', $sortOrder = 'ASC', $search = '')
    {
        $allowedCols = ['id', 'last_name', 'first_name', 'email', 'role', 'organization'];
        if (!in_array($sortCol, $allowedCols)) {
            $sortCol = 'last_name';
        }

        $sortOrder = strtoupper($sortOrder);
        if (!in_array($sortOrder, ['ASC', 'DESC'])) {
            $sortOrder = 'ASC';
        }

        $sql = "SELECT id, last_name, first_name, organization, email, phone, role FROM users";
        if (!empty($search)) {
            $sql .= " WHERE last_name LIKE ? OR first_name LIKE ? OR email LIKE ?";
        }
        $sql .= " ORDER BY $sortCol $sortOrder LIMIT ? OFFSET ?";

        $stmt = $this->db->prepare($sql);

        if (!empty($search)) {
            $wildcard = "%$search%";
            $stmt->bind_param("sssii", $wildcard, $wildcard, $wildcard, $limit, $offset);
        } else {
            $stmt->bind_param("ii", $limit, $offset);
        }

        $stmt->execute();
        return $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
    }

    public function getByEmail($email)
    {
        $stmt = $this->db->prepare("SELECT * FROM users WHERE email = ?");
        $stmt->bind_param("s", $email);
        $stmt->execute();
        return $stmt->get_result()->fetch_assoc();
    }
}
