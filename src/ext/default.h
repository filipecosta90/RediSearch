#ifndef __EXT_DEFAULT_H__
#define __EXT_DEFAULT_H__
#include "redisearch.h"

#define PHONETIC_EXPENDER_NAME "PHONETIC"
#define SYNONYMS_EXPENDER_NAME "SYNONYM"
#define STEMMER_EXPENDER_NAME "SBSTEM"
#define DEFAULT_EXPANDER_NAME "DEFAULT"
#define DEFAULT_SCORER_NAME "TFIDF"
#define TFIDF_DOCNORM_SCORER_NAME "TFIDF.DOCNORM"
#define DISMAX_SCORER_NAME "DISMAX"
#define BM25_SCORER_NAME "BM25"
#define DOCSCORE_SCORER "DOCSCORE"
#define HAMMINGDISTANCE_SCORER "HAMMING"

int DefaultExtensionInit(RSExtensionCtx *ctx);

typedef enum {
  /* Flag for scorer function to create explanation strings */
  SCORE_F_WITH_EXPLANATION = 0x01
} ScoreFuncFlags;

#endif