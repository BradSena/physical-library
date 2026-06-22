# Reconnaissance en cascade

1. Base locale : si EAN déjà connu, retour immédiat.
2. UPCitemdb : lookup EAN/UPC → nom produit.
3. BarcodeLookup : lookup EAN/UPC → nom produit.
4. Nettoyage titre/support.
5. TMDb : enrichissement titre/année/tmdb_id.
6. Score de confiance : validation automatique si >= 0.80, sinon manuel.

Fallback manuel : titre + année + support + emplacement origine. Le code-barres est mémorisé ensuite.
