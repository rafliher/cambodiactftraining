package main

import (
	"bufio"
	"crypto/md5"
	"crypto/sha1"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"
)

type FlagRequest struct {
	Flag string `json:"flag"`
}

var (
	validWordList = map[string]bool{}
	hashDB        = []string{
		"f3f0c6e992b7562598d9865b6fe8b3a6", 
		"aa8c41330509455ee5679d04ed41535d280d9a89",
		"ecb53f367b3541da3a14236d9a091f9bcc7a9903953f36577c2664fdd2a68a55",
		"67f2a835697e7c9c2c5146c76eca6038", 
		"91a8c384094a60c4e38e2741bb1462e2a3233c13",
		"f5d95c4771c4b0dc095c3cbb3a21396aaafd39d96eb0b55ff5077ccc050273f2",
		"afa8b5df937facadbba529e500e69a6e", 
		"2d231af11f9498ed68b39d752c4ac434c2e93ecd",
	}
)

func loadValidParts(filepath string) error {
	file, err := os.Open(filepath)
	if err != nil {
		return err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		word := strings.TrimSpace(scanner.Text())
		if word != "" {
			validWordList[word] = true
		}
	}

	return scanner.Err()
}

func hashAndCheck(part string, index int) bool {
	hashFuncs := []func([]byte) []byte{
		func(b []byte) []byte { h := md5.Sum(b); return h[:] },
		func(b []byte) []byte { h := sha1.Sum(b); return h[:] },
		func(b []byte) []byte { h := sha256.Sum256(b); return h[:] },
		func(b []byte) []byte { h := md5.Sum(b); return h[:] },
		func(b []byte) []byte { h := sha1.Sum(b); return h[:] },
		func(b []byte) []byte { h := sha256.Sum256(b); return h[:] },
		func(b []byte) []byte { h := md5.Sum(b); return h[:] },
		func(b []byte) []byte { h := sha1.Sum(b); return h[:] },
	}

	if index >= len(hashFuncs) || index >= len(hashDB) {
		return false // out of bounds
	}

	hash := hex.EncodeToString(hashFuncs[index]([]byte(part)))

	return hash == hashDB[index]
}

func flagHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Use POST", http.StatusMethodNotAllowed)
		return
	}

	var req FlagRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	if !strings.HasPrefix(req.Flag, "CNCC{") || !strings.HasSuffix(req.Flag, "}") {
		http.Error(w, "Flag must be in format CNCC{...}", http.StatusBadRequest)
		return
	}

	content := req.Flag[5 : len(req.Flag)-1]
	parts := strings.Split(content, "_")

	validCount := 0
	total := len(parts)

	for i, part := range parts {
		if validWordList[part] && hashAndCheck(part, i) {
			validCount++
		} 
	}

	result := map[string]interface{}{
		"valid_parts": validCount,
		"total_parts": total,
		"valid":     validCount == total,
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(result)
}

func printAPIDocs() {
	fmt.Println("🔥 CNCC Flag Checker API 🔥")
	fmt.Println("---------------------------")
	fmt.Println("Endpoint: POST /check-flag")
	fmt.Println("Request JSON format:")
	fmt.Println(`  {
    "flag": "CNCC{redacted}"
  }`)
	fmt.Println()
	fmt.Println("Flag rule:")
	fmt.Println("  - Must start with CNCC{ and end with }")
	fmt.Println()
	fmt.Println("Sample cURL:")
	fmt.Println(`  curl -X POST http://localhost:8080/check-flag \`)
	fmt.Println(`       -H "Content-Type: application/json" \`)
	fmt.Println(`       -d '{"flag": "CNCC{shield_flux_phase}"}'`)
	fmt.Println("---------------------------\n")
}
func main() {
	err := loadValidParts("flag.data")
	if err != nil {
		fmt.Println("Failed to load flag.data:", err)
		os.Exit(1)
	}

	http.HandleFunc("/check-flag", flagHandler)
	fmt.Println("Server running on http://localhost:8080")
	printAPIDocs()
	http.ListenAndServe(":8080", nil)
}
