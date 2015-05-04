from cloutron.view import *
from cloutron.plugin import *
import boto.ec2.elb
from time import localtime, strftime


class ElbView (TerminalView):

	@classmethod
	def configure_subparser(cls, subparsers):
		sp = subparsers.add_parser('elasticloadbalancers', help='display elastic load balancer statuses', aliases=('elb','lb','e'))
		CloutronView.add_generic_arguments(sp)
		sp.set_defaults(func=ElbView)
		sp.add_argument('--show-instances', '-i', dest="display_instances", action="store_true", help="display ELB instances (Default)", default=None)
		sp.add_argument("--hide-instances", '-I', dest="display_instances", action="store_false", help="do not display ELB instances")
		
	def apply_cli_config(self):
		super(ElbView, self).apply_cli_config()
		if self.args.display_instances != None:
		    self.config.display_instances = self.args.display_instances

	def sigwinch_handler(self, sig, stack):
		self.render()
		
	def render(self):
		self.info = "ELBs [%s]" % self.config.region
		self.title = "[Updated " + strftime("%H:%M:%S", localtime()) + "] Cloutron"
		self.do_render("Loading....")
		while True:
			conn = boto.ec2.elb.connect_to_region(self.config.region)
			res = conn.get_all_load_balancers()
			output = self.colour("", "white", "grey", [])
			for r in res:
				allinstances = 0
				upinstances = 0
				output = output + "%s (%s)" % (r.name, r.dns_name)
				output2 = ""
				for i in r.get_instance_health():
					allinstances += 1
					stateoutput = ""
					if i.state == "OutOfService":
						stateoutput = self.colour("Out of Service", "red", "grey", [])
					if i.state == "InService":
						upinstances += 1
						stateoutput = self.colour("In Service", "green", "grey", [])
					else:
						stateoutput = i.state

					if self.config.display_instances:
						output2 = output2 + "\n - %s (%s)" % (i.instance_id, stateoutput)
				output = output + " [up:%s down:%s]" % (upinstances, allinstances-upinstances)
				output = output + output2
				output = output + "\n"

			self.title = "[Updated " + strftime("%H:%M:%S", localtime()) + "] Cloutron"
			self.do_render(output)
			if float(self.config.poll) < 30:
				time.sleep(30)
			else:
				time.sleep(float(self.config.poll))

class ElbViewPlugin(ViewPlugin):
	plugin_type = 'view'
	name = 'elb'
	view_class = ElbView
