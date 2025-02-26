import os

from django.test import TestCase

from beagle.settings import ROOT_DIR
from beagle_etl.models import Operator
from runner.operator.operator_factory import OperatorFactory
from file_system.repository.file_repository import FileRepository
from runner.operator.access.v1_0_0.snps_and_indels import AccessLegacySNVOperator



REQUEST_ID = "access_legacy_test_request"
TEST_RUN_ID = 'bc23076e-f477-4578-943c-1fbf6f1fca44'
FIXTURES = [
    "fixtures/tests/access_snv/curated_normal_files.json",
    "fixtures/tests/access_snv/curated_normals_file_metadata.json",
    "fixtures/tests/access_snv/files.json",
    "fixtures/tests/access_snv/files_metadata.json",
    "fixtures/tests/access_snv/operator_run.json",
    "fixtures/tests/access_snv/ports.json",
    "fixtures/tests/access_snv/runs.json",
]

COMMON_FIXTURES = [
    'runner/fixtures/runner.pipeline.json',
    'runner/fixtures/runner.run.json',
    'runner/fixtures/runner.operator_run.json',
    'file_system/fixtures/file_system.filegroup.json',
    'file_system/fixtures/file_system.filetype.json',
    'file_system/fixtures/file_system.storage.json',
    'beagle_etl/fixtures/beagle_etl.operator.json',
]


class TestAccessSNVOperator(TestCase):

    fixtures = [os.path.join(ROOT_DIR, f) for f in FIXTURES + COMMON_FIXTURES]

    def test_access_legacy_snv_operator(self):
        """
        Test that an Access legacy SNV operator instance can be created and validated
        """
        # create access SNV operator
        # todo: avoid the magic number here:
        operator_model = Operator.objects.get(id=5)
        operator = OperatorFactory.get_by_model(operator_model, request_id=REQUEST_ID)
        self.assertEqual(operator.get_pipeline_id(), "65419097-a2b8-4d57-a8ab-c4c4cddcbeaa")
        self.assertEqual(str(operator.model), "AccessLegacySNVOperator")
        self.assertEqual(operator.request_id, REQUEST_ID)
        self.assertEqual(operator._jobs, [])

        pipeline_slug = "AccessLegacySNVOperator"
        access_legacy_snv_model = Operator.objects.get(slug=pipeline_slug)
        operator = AccessLegacySNVOperator(access_legacy_snv_model, request_id=REQUEST_ID, run_ids=['bc23076e-f477-4578-943c-1fbf6f1fca44'])

        self.assertTrue(isinstance(operator, AccessLegacySNVOperator))
        self.assertTrue(operator.request_id == REQUEST_ID)
        self.assertTrue(operator._jobs == [])
        self.assertEqual(operator.run_ids, ['bc23076e-f477-4578-943c-1fbf6f1fca44'])
        self.assertEqual(operator.get_pipeline_id(), "65419097-a2b8-4d57-a8ab-c4c4cddcbeaa")

        # Create and validate the input data
        input_data = operator.get_sample_inputs()
        self.validate(input_data)

    def test_dmp_normal(self):
        """
        Test that DMP normal can be found and used for an SNV Request ID

        :return:
        """
        # Delete the IGO test samples, so DMP normal must be used
        metadatas = FileRepository.filter(path_regex='C-000884', metadata={"tumorOrNormal": "Normal"})
        [f.file.delete() for f in metadatas]

        pipeline_slug = "AccessLegacySNVOperator"
        access_legacy_snv_model = Operator.objects.get(slug=pipeline_slug)
        operator = AccessLegacySNVOperator(access_legacy_snv_model, request_id=REQUEST_ID, run_ids=[TEST_RUN_ID])
        input_data = operator.get_sample_inputs()

        geno_bams = [b['location'] for b in input_data[0]['genotyping_bams']]
        self.assertTrue(any('AA037277-N-unfilter.bam' in b for b in geno_bams))

    def test_run_on_imported_bams(self):
        """
        Test that the inputs are generated for a set of bams that was manually imported

        :return:
        """
        pipeline_slug = "AccessLegacySNVOperator"
        request_id = 'access_legacy_test_request_imported_bams'
        test_run_id = 'bc23076e-f477-4578-943c-1fbf6f1fca42'
        access_legacy_snv_model = Operator.objects.get(slug=pipeline_slug)
        operator = AccessLegacySNVOperator(access_legacy_snv_model, request_id=request_id, run_ids=[test_run_id])
        input_data = operator.get_sample_inputs()
        self.validate(input_data)

    def validate(self, input_data):
        # Only a single entry is required in these fields, as we are running in single-sample mode
        required_input_fields = [
            'tumor_bams',
            'normal_bams',
            'tumor_sample_names',
            'normal_sample_names',
            'matched_normal_ids',
        ]

        # We should have 9 bams for genotyping:
        # - Main Tumor Bam Duplex
        # - Main Tumor Bam Simplex
        # - Default Variant Calling Normal Duplex
        # - Matched Normal Duplex
        # - Matched Normal Simplex
        # - Matched Tumor Duplex IGO
        # - Matched Tumor Simplex IGO
        # - Matched Tumor Duplex DMP
        # - Matched Tumor Simplex DMP
        required_input_fields_length_9 = [
            'genotyping_bams',
            'genotyping_bams_ids',
        ]

        for inputs in input_data:
            for field in required_input_fields:
                self.assertIn(field, inputs)
                self.assertEqual(len(inputs[field]), 1)
            for field in required_input_fields_length_9:
                self.assertIn(field, inputs)
                self.assertEqual(len(inputs[field]), 9)
